"""Check the explicitly owned documentation, CI and pre-push entry blocks.

This checks a fixed repository format, not arbitrary Markdown, YAML or shell.
Historical examples and focused checker commands are outside these blocks.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMAND = 'python scripts/check_docs.py'
DOCS = ('docs/documentation.md', 'docs/documentation.zh.md')
START = '<!-- doc-check-entry -->'
END = '<!-- /doc-check-entry -->'
DOC_BLOCK = START + '\n```sh\n' + COMMAND + '\n```\n' + END
CI_STEPS = (
    ('Verify documentation entry wiring', 'python scripts/check_doc_entry.py'),
    ('Run Python documentation checks', COMMAND),
)
HOOK = '#!/bin/sh\n# Shared Python documentation checks; run from the repository root.\n' + COMMAND + '\n'


def check(root=ROOT):
    errors = []
    for name in DOCS:
        text = (root / name).read_text(encoding='utf-8')
        if text.count(START) != 1 or text.count(END) != 1 or DOC_BLOCK not in text:
            errors.append(f'{name}: expected one documented entry: {COMMAND}')
    text = (root / '.github/workflows/docs.yml').read_text(encoding='utf-8')
    # Require complete, unconditional steps, not a command in a comment or
    # a step with continue-on-error. Pin only these two owned step blocks.
    steps = re.findall(r'^      - name: ([^\n]+)\n((?:(?!      - ).*\n?)*)', text, re.M)
    for name, command in CI_STEPS:
        bodies = [body.rstrip() for title, body in steps if title == name]
        if bodies != ['        run: ' + command]:
            errors.append(f'.github/workflows/docs.yml: expected unconditional step {name}: {command}')
    if (root / '.githooks/pre-push').read_text(encoding='utf-8') != HOOK:
        errors.append('.githooks/pre-push: expected shared Python documentation entry')
    if not (root / 'scripts/check_docs.py').is_file():
        errors.append('scripts/check_docs.py: missing entry')
    return errors


def main():
    try:
        errors = check()
    except (OSError, UnicodeError) as error:
        errors = [str(error)]
    for error in errors:
        print(error, file=sys.stderr)
    print(f'Documentation entry: {len(errors)} error(s).')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
