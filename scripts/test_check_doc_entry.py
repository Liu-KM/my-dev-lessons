"""Inject three faults into a disposable checkout and run real entry commands."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from check_doc_entry import ROOT, COMMAND, check


class EntryExperiments(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('scripts', 'docs', 'lessons', 'templates', '.github', '.githooks'):
            # Do not copy this integration suite: the child runner executes the
            # existing regression tests, without recursively spawning itself.
            shutil.copytree(ROOT / name, self.root / name,
                            ignore=shutil.ignore_patterns('__pycache__', 'test_check_doc_entry.py'))
        for path in ROOT.glob('*.md'):
            shutil.copyfile(path, self.root / path.name)

    def run_entry(self, script='check_docs.py'):
        return subprocess.run([sys.executable, '-B', str(self.root / 'scripts' / script)],
                              cwd=self.root, capture_output=True, encoding='utf-8',
                              errors='replace', timeout=60)

    def experiment(self, name, relative, transform, diagnostic, script='check_docs.py'):
        path = self.root / relative
        original = path.read_bytes()
        before = self.run_entry()
        self.assertEqual(before.returncode, 0, before.stdout + before.stderr)
        changed = transform(original.decode('utf-8'))
        self.assertNotEqual(changed, original.decode('utf-8'))
        try:
            path.write_text(changed, encoding='utf-8')
            broken = self.run_entry(script)
            self.assertNotEqual(broken.returncode, 0, broken.stdout + broken.stderr)
            self.assertIn(diagnostic, broken.stdout + broken.stderr)
            print(f'{name}: baseline={before.returncode}, fault={broken.returncode}; {diagnostic}', flush=True)
        finally:
            path.write_bytes(original)
        repaired = self.run_entry()
        self.assertEqual(repaired.returncode, 0, repaired.stdout + repaired.stderr)
        self.assertEqual(path.read_bytes(), original)
        print(f'{name}: repaired={repaired.returncode}', flush=True)

    def test_documented_command_then_repair(self):
        self.experiment('documented command', 'docs/documentation.zh.md',
                        lambda text: text.replace(COMMAND, 'python scripts/check_docz.py'),
                        'expected one documented entry')

    def test_missing_lesson_section_then_repair(self):
        self.experiment('missing lesson section', 'lessons/docs-example-typecheck.md',
                        lambda text: text.replace('## Method', '### Method'),
                        'docs-example-typecheck.md:')

    def test_ci_bypass_then_repair(self):
        self.experiment('CI bypass', '.github/workflows/docs.yml',
                        lambda text: text.replace(COMMAND, 'python scripts/check_lessons.py'),
                        'expected unconditional step Run Python documentation checks',
                        script='check_doc_entry.py')

    def test_disabling_step_and_missing_document_marker_are_rejected(self):
        workflow = self.root / '.github/workflows/docs.yml'
        workflow.write_text(workflow.read_text(encoding='utf-8').replace(
            '      - name: Run Python documentation checks\n',
            '      - name: Run Python documentation checks\n        if: false\n'), encoding='utf-8')
        self.assertTrue(check(self.root))
        document = self.root / 'docs/documentation.md'
        document.write_text(document.read_text(encoding='utf-8').replace(
            '<!-- doc-check-entry -->', ''), encoding='utf-8')
        self.assertTrue(any('documentation.md:' in error for error in check(self.root)))


if __name__ == '__main__':
    unittest.main()
