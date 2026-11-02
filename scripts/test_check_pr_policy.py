from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

import check_pr_policy as policy
from check_pr_policy import metadata_errors, stack_errors


class PRPolicyTests(unittest.TestCase):
    def setUp(self):
        self.labels = {'kind/feature': '', 'kind/doc': '', 'area/docs': ''}
        self.pr = {'labels': [{'name': 'kind/feature'}, {'name': 'area/docs'}],
                   'body': '## Motivation\nRefs #12\n\n## Changes\nAdd a check.\n\n## Testing\nUnit tests passed.'}

    def test_valid_issue_and_labels(self):
        seen = []
        self.assertEqual(metadata_errors(self.pr, self.labels, lambda n: seen.append(n) or {}), [])
        self.assertEqual(seen, [12])

    def test_pr_number_is_not_issue(self):
        self.assertTrue(metadata_errors(self.pr, self.labels, lambda n: {'pull_request': {}}))

    def test_hidden_references_do_not_count(self):
        for hidden in ('<!-- Refs #12 -->', '`Refs #12`', '```text\nRefs #12\n```', '> Refs #12'):
            self.pr['body'] = '## Motivation\nReason\n' + hidden + '\n## Changes\nChange\n## Testing\nTests'
            self.assertTrue(metadata_errors(self.pr, self.labels, lambda n: {}))

    def test_missing_multiple_and_unknown_labels(self):
        for names in ([], ['kind/doc'], ['kind/doc', 'kind/feature', 'area/docs'], ['kind/doc', 'area/unknown']):
            self.pr['labels'] = [{'name': name} for name in names]
            self.assertTrue(metadata_errors(self.pr, self.labels, lambda n: {}))

    def test_empty_template_section(self):
        self.pr['body'] = self.pr['body'].replace('Add a check.', '<!-- Fill changes -->')
        self.assertTrue(metadata_errors(self.pr, self.labels, lambda n: {}))

    def test_native_stack_order(self):
        pr = {'head': {'repo': {'full_name': 'owner/repo'}}, 'base': {'repo': {'full_name': 'owner/repo'}}}
        parent = {'number': 1}
        info = lambda number, position: {'stack': {'number': number, 'baseRefName': 'main'}, 'stackEntry': {'position': position}}
        self.assertEqual(stack_errors(pr, parent, info(5, 2), info(5, 1), 'main'), [])
        self.assertTrue(stack_errors(pr, parent, info(6, 2), info(5, 1), 'main'))
        self.assertTrue(stack_errors(pr, parent, info(5, 3), info(5, 1), 'main'))
        self.assertTrue(stack_errors(pr, parent, {}, {}, 'main'))
        self.assertTrue(stack_errors(pr, None, {}, {}, 'main'))
        pr['head']['repo']['full_name'] = 'fork/repo'
        self.assertTrue(stack_errors(pr, parent, info(5, 2), info(5, 1), 'main'))


class PRPolicyEntryTests(unittest.TestCase):
    """Run the production entry and HTTP adapter without contacting GitHub."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.event_path = Path(directory.name) / 'event.json'
        self.event = {'pull_request': {'number': 12, 'draft': True, 'labels': []}}
        self.pr = {
            'number': 12, 'state': 'open', 'draft': False,
            'labels': [{'name': 'kind/doc'}, {'name': 'area/docs'}],
            'body': '## Motivation\nClarify collaboration.\nRefs #2\n\n## Changes\nAdd policy.\n\n## Testing\nLocal tests passed.',
            'head': {'repo': {'full_name': 'owner/repo'}, 'ref': 'feature'},
            'base': {'repo': {'full_name': 'owner/repo'}, 'ref': 'main'},
        }
        self.routes = {
            '/repos/owner/repo/pulls/12': self.pr,
            '/repos/owner/repo/issues/2': {'number': 2},
            '/repos/owner/repo': {'default_branch': 'main'},
            '/repos/owner/repo/pulls': [{'number': 10}],
        }
        self.calls = []
        self.env = {
            'GITHUB_REPOSITORY': 'owner/repo',
            'GITHUB_EVENT_PATH': str(self.event_path),
            'GITHUB_API_URL': 'https://api.github.test',
            'GH_TOKEN': 'test-only-token',
        }
        self.graphql_error = False

    def respond(self, request, timeout):
        self.assertEqual(timeout, 30)
        self.assertEqual(request.get_header('Authorization'), 'Bearer test-only-token')
        url = urlsplit(request.full_url)
        self.assertEqual(url.netloc, 'api.github.test')
        self.calls.append(url.path)
        if url.path == '/graphql':
            self.assertEqual(request.get_method(), 'POST')
            payload = json.loads(request.data)
            self.assertEqual(payload['variables']['owner'], 'owner')
            self.assertEqual(payload['variables']['name'], 'repo')
            number = payload['variables']['number']
            self.assertIn(number, (10, 12))
            if self.graphql_error:
                result = {'errors': [{'message': 'Resource not accessible'}]}
            else:
                result = {'data': {'repository': {'pullRequest': {
                    'stack': {'number': 7, 'baseRefName': 'main'},
                    'stackEntry': {'position': 2 if number == 12 else 1},
                }}}}
        else:
            self.assertEqual(request.get_method(), 'GET')
            if url.path.endswith('/pulls'):
                self.assertEqual(parse_qs(url.query)['head'], ['owner:parent'])
                self.assertEqual(parse_qs(url.query)['state'], ['open'])
            result = self.routes[url.path]
            if isinstance(result, Exception):
                raise result
        return io.BytesIO(json.dumps(result).encode())

    def invoke(self):
        self.event_path.write_text(json.dumps(self.event), encoding='utf-8')
        output, errors = io.StringIO(), io.StringIO()
        with patch.dict(os.environ, self.env), patch.object(policy, 'urlopen', side_effect=self.respond), \
                redirect_stdout(output), redirect_stderr(errors):
            code = policy.run()
        return code, output.getvalue(), errors.getvalue()

    def test_pr_event_uses_live_metadata_not_event_snapshot(self):
        code, output, errors = self.invoke()
        self.assertEqual(code, 0, errors)
        self.assertIn('0 policy error(s)', output)
        self.assertIn('/repos/owner/repo/issues/2', self.calls)
        self.assertNotIn('/graphql', self.calls)

    def test_manual_dispatch(self):
        self.event = {'inputs': {'pr_number': '12'}}
        self.assertEqual(self.invoke()[0], 0)

    def test_draft_and_closed_prs_are_explicitly_deferred(self):
        for state, draft in (('open', True), ('closed', False)):
            with self.subTest(state=state, draft=draft):
                self.pr.update(state=state, draft=draft)
                self.calls.clear()
                code, output, errors = self.invoke()
                self.assertEqual(code, 0, errors)
                self.assertIn('deferred', output)
                self.assertEqual(self.calls, ['/repos/owner/repo/pulls/12'])

    def test_invalid_metadata_returns_failure(self):
        self.pr['labels'] = []
        code, output, _ = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn('Select exactly one kind/*', output)

    def test_missing_issue_and_permission_error_fail_closed(self):
        for path, status in (('/repos/owner/repo/issues/2', 404),
                             ('/repos/owner/repo/pulls/12', 403)):
            with self.subTest(status=status):
                original = self.routes[path]
                self.routes[path] = HTTPError('https://api.github.test' + path, status, 'Denied', {}, None)
                code, _, errors = self.invoke()
                self.assertEqual(code, 1)
                self.assertIn(str(status), errors)
                self.assertNotIn(self.env['GH_TOKEN'], errors)
                self.routes[path] = original

    def test_transport_failure_is_not_success(self):
        for error in (URLError('offline'), TimeoutError('timed out')):
            with self.subTest(error=type(error).__name__):
                self.routes['/repos/owner/repo/pulls/12'] = error
                code, _, errors = self.invoke()
                self.assertEqual(code, 1)
                self.assertIn('Policy could not be verified', errors)

    def test_dependent_pr_fetches_parent_and_both_stack_entries(self):
        self.pr['base']['ref'] = 'parent'
        code, _, errors = self.invoke()
        self.assertEqual(code, 0, errors)
        self.assertEqual(self.calls.count('/graphql'), 2)

    def test_missing_or_ambiguous_parent_fails(self):
        self.pr['base']['ref'] = 'parent'
        for parents in ([], [{'number': 10}, {'number': 11}]):
            with self.subTest(parents=parents):
                self.routes['/repos/owner/repo/pulls'] = parents
                self.calls.clear()
                code, output, _ = self.invoke()
                self.assertEqual(code, 1)
                self.assertIn('exactly one open parent PR', output)
                self.assertNotIn('/graphql', self.calls)

    def test_graphql_error_is_not_a_valid_stack(self):
        self.pr['base']['ref'] = 'parent'
        self.graphql_error = True
        code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn('Native stack API unavailable', errors)

    def test_invalid_input_fails_before_network_access(self):
        for value in (None, '', '0', '-1', 'abc'):
            with self.subTest(value=value):
                self.event = {'inputs': {'pr_number': value}}
                self.calls.clear()
                code, _, errors = self.invoke()
                self.assertEqual(code, 1)
                self.assertIn('positive PR number', errors)
                self.assertEqual(self.calls, [])

    def test_cli_process_exits_nonzero_on_invalid_event(self):
        self.event_path.write_text('{}', encoding='utf-8')
        result = subprocess.run([sys.executable, str(policy.ROOT / 'scripts/check_pr_policy.py')],
                                env={**os.environ, **self.env}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('positive PR number', result.stderr)


if __name__ == '__main__':
    unittest.main()
