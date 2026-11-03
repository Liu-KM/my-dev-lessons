"""Exercise the real CLI on isolated files, including its semantic limits."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from check_doc_budgets import ROOT, count_units


class DocumentationBudgets(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        self.script = self.root / 'scripts/check_doc_budgets.py'
        shutil.copyfile(ROOT / 'scripts/check_doc_budgets.py', self.script)
        self.manifest = self.root / 'scripts/doc-budgets.manifest.json'
        self.doc = self.root / 'AGENTS.md'
        self.doc.write_text('one two', encoding='utf-8')
        self.configure({'AGENTS.md': {'metric': 'words', 'max': 2}})

    def configure(self, value):
        self.manifest.write_text(json.dumps(value), encoding='utf-8')

    def run_cli(self, *args):
        # Running elsewhere verifies that file resolution follows the script,
        # not the caller's current directory.
        return subprocess.run([sys.executable, '-B', str(self.script), *args],
                              cwd=self.root.parent, capture_output=True,
                              encoding='utf-8', timeout=10)

    def test_at_ceiling_overflow_then_repair_without_rewriting(self):
        original_manifest = self.manifest.read_bytes()
        self.assertEqual(self.run_cli().returncode, 0)
        self.doc.write_text('one two three', encoding='utf-8')
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn('AGENTS.md: 3 words exceeds 2', result.stderr)
        self.assertEqual(self.doc.read_text(encoding='utf-8'), 'one two three')
        self.assertEqual(self.manifest.read_bytes(), original_manifest)
        self.doc.write_text('one two', encoding='utf-8')
        self.assertEqual(self.run_cli().returncode, 0)

    def test_chinese_overflow_without_spaces(self):
        self.configure({'AGENTS.md': {'metric': 'characters', 'max': 4}})
        self.doc.write_text('规则唯一\n', encoding='utf-8')
        self.assertEqual(self.run_cli().returncode, 0)
        self.doc.write_text('规则唯一性\n', encoding='utf-8')
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn('5 characters exceeds 4', result.stderr)

    def test_whole_file_metrics_include_code_and_normalize_whitespace(self):
        self.assertEqual(count_units('# Guide\r\n\n```py\nprint(1)\n```\n', 'words'), 5)
        self.assertEqual(count_units('规则 CI\r\n🙂', 'characters'), 5)
        self.assertEqual(count_units('a\tb\r\nc', 'words'), 3)

    def test_missing_listed_file_fails(self):
        self.doc.rename(self.root / 'renamed.md')
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn('AGENTS.md: budgeted file does not exist', result.stderr)

    def test_invalid_entries_fail(self):
        for entry in (2, {'metric': 'tokens', 'max': 2},
                      {'metric': 'words'}, {'max': 2},
                      *({'metric': 'words', 'max': value}
                        for value in (True, 0, -1, 1.5, '2'))):
            with self.subTest(entry=entry):
                self.configure({'AGENTS.md': entry})
                result = self.run_cli()
                self.assertEqual(result.returncode, 1)
                self.assertIn('AGENTS.md:', result.stderr)

    def test_missing_or_malformed_manifest_fails(self):
        self.manifest.unlink()
        self.assertEqual(self.run_cli().returncode, 1)
        self.manifest.write_text('{', encoding='utf-8')
        self.assertEqual(self.run_cli().returncode, 1)
        self.configure([])
        self.assertEqual(self.run_cli().returncode, 1)

    def test_list_is_diagnostic_not_an_enforcement_command(self):
        self.doc.write_text('one two three', encoding='utf-8')
        self.configure({'AGENTS.md': {'metric': 'words', 'max': 2},
                        'missing.md': {'metric': 'words', 'max': 2}})
        result = self.run_cli('--list')
        self.assertEqual(result.returncode, 0)
        self.assertIn('OVER: AGENTS.md: 3/2 words', result.stdout)
        self.assertIn('ERROR: missing.md:', result.stdout)
        self.assertEqual(self.run_cli().returncode, 1)

    def test_unlisted_reference_is_not_budgeted(self):
        (self.root / 'reference.md').write_text('fact ' * 1000, encoding='utf-8')
        self.assertEqual(self.run_cli().returncode, 0)

    def test_short_conflict_is_not_detected(self):
        self.configure({'AGENTS.md': {'metric': 'words', 'max': 10}})
        self.doc.write_text('Always require review. Never require review.', encoding='utf-8')
        self.assertEqual(self.run_cli().returncode, 0)


if __name__ == '__main__':
    unittest.main()
