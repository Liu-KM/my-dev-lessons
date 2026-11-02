"""Read-only PR metadata checks, run from the trusted default branch in CI."""

import json
import os
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def visible_body(body):
    body = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    lines, fence = [], None
    for line in body.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        elif not line.lstrip().startswith('>'):
            lines.append(re.sub(r"(`+).*?\1", "", line))
    return "\n".join(lines)


def metadata_errors(pr, labels, get_issue):
    errors = []
    names = [label['name'] for label in pr['labels']]
    kinds = [name for name in names if name.startswith('kind/')]
    areas = [name for name in names if name.startswith('area/')]
    if len(kinds) != 1:
        errors.append('Select exactly one kind/* label.')
    if not areas:
        errors.append('Select at least one area/* label.')
    unknown = set(kinds + areas) - labels.keys()
    if unknown:
        errors.append('Unknown labels: ' + ', '.join(sorted(unknown)))
    body = visible_body(pr.get('body'))
    for heading in ('Motivation', 'Changes', 'Testing'):
        section = re.search(r'^## ' + heading + r'\s*\n(.*?)(?=^## |\Z)', body, re.M | re.S)
        if not section or not section[1].strip():
            errors.append(f'Fill in ## {heading}.')
    numbers = sorted({int(n) for n in re.findall(
        r'(?im)^\s*(?:[-*]\s+)?(?:refs|fix(?:es|ed)?|close[sd]?|resolve[sd]?)\s+#([1-9]\d*)\b', body)})
    if not numbers:
        errors.append('Add a standalone Refs #N or Fixes #N line for a same-repository Issue.')
    for number in numbers:
        issue = get_issue(number)
        if issue.get('pull_request') is not None:
            errors.append(f'#{number} is a PR, not an Issue.')
    return errors


def stack_errors(pr, parent, child_stack, parent_stack, trunk):
    errors = []
    if pr['head']['repo']['full_name'] != pr['base']['repo']['full_name']:
        return ['Dependent PRs require same-repository branches.']
    if parent is None:
        return ['Non-trunk base must be the head of exactly one open parent PR.']
    child = child_stack.get('stack')
    owner = parent_stack.get('stack')
    a, b = child_stack.get('stackEntry'), parent_stack.get('stackEntry')
    if not child or not owner or not a or not b:
        return ['Link dependent PRs into a native GitHub stack.']
    if child['number'] != owner['number'] or child['baseRefName'] != trunk:
        errors.append('Parent and child must share a native stack targeting the default branch.')
    if a['position'] != b['position'] + 1:
        errors.append('Native stack order must match the immediate parent branch.')
    return errors


def api(path, data=None):
    request = Request(os.environ.get('GITHUB_API_URL', 'https://api.github.com') + path,
                      data=None if data is None else json.dumps(data).encode(),
                      headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                               'Accept': 'application/vnd.github+json',
                               'Content-Type': 'application/json'})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def native_stack(repo, number):
    owner, name = repo.split('/')
    result = api('/graphql', {'query': '''query($owner:String!,$name:String!,$number:Int!) {
      repository(owner:$owner,name:$name) { pullRequest(number:$number) {
        stack { number baseRefName } stackEntry { position }
      } }
    }''', 'variables': {'owner': owner, 'name': name, 'number': number}})
    if result.get('errors'):
        raise RuntimeError('Native stack API unavailable or denied; cannot verify dependent PR.')
    return result['data']['repository']['pullRequest']


def main():
    repo = os.environ['GITHUB_REPOSITORY']
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
    number = event.get('pull_request', {}).get('number') or event.get('inputs', {}).get('pr_number')
    if not re.fullmatch(r'[1-9]\d*', str(number)):
        raise ValueError('Provide a positive PR number in the event or pr_number input.')
    number = int(number)
    pr = api(f'/repos/{repo}/pulls/{number}')
    if pr['state'] != 'open' or pr['draft']:
        print('Draft or closed PR: policy deferred until ready for review.')
        return 0
    labels = json.loads((ROOT / '.github/pr-labels.json').read_text(encoding='utf-8'))
    errors = metadata_errors(pr, labels, lambda n: api(f'/repos/{repo}/issues/{n}'))
    trunk = api(f'/repos/{repo}')['default_branch']
    if pr['base']['ref'] != trunk:
        from urllib.parse import urlencode
        query = urlencode({'state': 'open', 'head': repo.split('/')[0] + ':' + pr['base']['ref'], 'per_page': 100})
        parents = api(f'/repos/{repo}/pulls?{query}')
        parent = parents[0] if len(parents) == 1 else None
        errors += stack_errors(pr, parent, native_stack(repo, number) if parent else {},
                               native_stack(repo, parent['number']) if parent else {}, trunk)
    for error in errors:
        print('ERROR: ' + error)
    print(f'PR #{number}: {len(errors)} policy error(s).')
    return bool(errors)


def run():
    """The CLI boundary: an unavailable check must exit unsuccessfully."""
    try:
        return int(main())
    except Exception as error:
        print(f'Policy could not be verified: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(run())
