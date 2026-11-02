import os
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path
import unittest

from check_lesson_pairs import ROOT, SECTION_KEYS, check_directory, pair_paths, record_text, validate_pair


class PairChecks(unittest.TestCase):
    def test_translated_prose_and_reordered_literals(self):
        self.assertEqual(validate_pair('Run `a` then `b`.', '先看 `b`，再看 `a`。'), [])

    def test_translated_inline_command(self):
        self.assertTrue(validate_pair('Run `doc-sync`.', '运行 `文档同步`。'))

    def test_deleted_or_duplicated_literal(self):
        self.assertTrue(validate_pair('`doc-sync`', '文档同步'))
        self.assertTrue(validate_pair('`doc-sync`', '`doc-sync` `doc-sync`'))

    def test_changed_fenced_command_and_language(self):
        sample = '```sh\npnpm run doc-sync\n```'
        self.assertEqual(validate_pair(sample, sample), [])
        self.assertTrue(validate_pair(sample, sample.replace('doc-sync', '文档同步')))
        self.assertTrue(validate_pair(sample, sample.replace('sh', 'text')))

    def test_literal_moved_to_another_section(self):
        self.assertTrue(validate_pair('## A\n`x`\n## B\n', '## 甲\n## 乙\n`x`'))

    def test_multibacktick_span_and_tilde_fence(self):
        sample = '``a ` b``\n~~~sh\necho x\n~~~'
        self.assertEqual(validate_pair(sample, sample), [])
        self.assertTrue(validate_pair(sample, sample.replace('echo x', 'echo y')))

    def test_malformed_code(self):
        self.assertTrue(validate_pair('`open', '`open'))
        self.assertTrue(validate_pair('```sh\nx', '```sh\nx'))

    def test_same_invalid_command_is_not_existence_validation(self):
        sample = '`pnpm run nonexistent-command`'
        self.assertEqual(validate_pair(sample, sample), [])

    def test_missing_counterpart(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'sample.md').write_text('`x`', encoding='utf-8')
            self.assertTrue(check_directory(root))
            (root / 'sample.zh.md').write_text('`x`', encoding='utf-8')
            # Both files exist, but a pair still needs valid lesson content and a record.
            self.assertTrue(check_directory(root))
            (root / 'sample.md').unlink()
            self.assertTrue(check_directory(root))


class RecordedPairChecks(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / 'lessons').mkdir()
        (self.root / 'scripts').mkdir()
        for name in ('check_lesson_pairs.py', 'check_lessons.py'):
            shutil.copyfile(ROOT / 'scripts' / name, self.root / 'scripts' / name)
        self.english = self.make_pair('sample')
        _, self.chinese, self.record = pair_paths(self.english)

    def make_pair(self, name):
        english = self.root / 'lessons' / (name + '.md')
        for file, original in zip(pair_paths(english)[:2], ('docs-example-typecheck.md', 'docs-example-typecheck.zh.md')):
            text = (ROOT / 'lessons' / original).read_text(encoding='utf-8')
            file.write_text(text.replace('docs-example-typecheck.', name + '.'), encoding='utf-8')
        return english

    def command(self, *args):
        return subprocess.run([sys.executable, str(self.root / 'scripts/check_lesson_pairs.py'), *args],
                              cwd=self.root, capture_output=True, text=True, encoding='utf-8',
                              env={**os.environ, 'PYTHONUTF8': '1'})

    def write_record(self, english=None):
        path = english or self.english
        result = self.command('--write', str(path))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def change(self, path, old, new):
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding='utf-8')

    def test_cli_edit_review_record_cycle(self):
        self.assertNotEqual(self.command().returncode, 0)
        self.write_record()
        self.assertEqual(self.command().returncode, 0)
        saved = self.record.read_bytes()
        self.change(self.english, '## Lesson', 'Check the changed examples.\n\n## Lesson')
        failed = self.command()
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('problem', failed.stdout)
        self.assertEqual(self.record.read_bytes(), saved, 'Read-only checks must not refresh hashes')
        self.change(self.chinese, '## 经验', '检查修改后的示例。\n\n## 经验')
        self.assertNotEqual(self.command().returncode, 0, 'Editing both sides still needs confirmation')
        self.write_record(self.chinese)
        self.assertEqual(self.command().returncode, 0)

    def test_only_edited_section_changes_record(self):
        self.write_record()
        before = self.record.read_text().splitlines()
        self.change(self.english, '## Case', 'Review the result.\n\n## Case')
        self.change(self.chinese, '## 案例', '审阅结果。\n\n## 案例')
        self.write_record()
        after = self.record.read_text().splitlines()
        changes = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
        index = 2 + SECTION_KEYS.index('method') * 3
        self.assertEqual(changes, [index + 1, index + 2])

    def test_title_and_chinese_only_edits_are_detected(self):
        self.write_record()
        self.change(self.chinese, '# 文档代码示例类型检查', '# 文档示例检查')
        result = self.command()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('intro', result.stdout)

    def test_code_stays_hashed_even_when_both_sides_change(self):
        self.write_record()
        for path in (self.english, self.chinese):
            self.change(path, '`doc-sync`', '`doc-sync-new`')
        self.assertNotEqual(self.command().returncode, 0)

    def test_invalid_pairs_cannot_be_confirmed(self):
        for language, old, new in (
            ('en', 'English | [中文](sample.zh.md)', 'English'),
            ('zh', '[English](sample.md) | 中文', '中文'),
            ('en', '## Method', '### Method'),
            ('zh', '`doc-sync`', '`文档同步`'),
        ):
            with self.subTest(language=language, old=old):
                path = self.english if language == 'en' else self.chinese
                original = path.read_bytes()
                self.change(path, old, new)
                self.assertNotEqual(self.command('--write', str(self.english)).returncode, 0)
                self.assertFalse(self.record.exists())
                path.write_bytes(original)

    def test_explicit_scope_and_no_partial_write(self):
        other = self.make_pair('other')
        self.write_record(other)
        other_record = pair_paths(other)[2]
        saved = other_record.read_bytes()
        self.change(other, '## Lesson', 'Unreviewed change.\n\n## Lesson')
        self.assertNotEqual(self.command('--write').returncode, 0)
        self.assertEqual(other_record.read_bytes(), saved)
        self.write_record()
        self.assertEqual(self.command(str(self.english)).returncode, 0)
        self.assertNotEqual(self.command().returncode, 0)
        self.assertEqual(other_record.read_bytes(), saved)
        self.change(self.english, '## Lesson', '## Missing')
        result = self.command('--write', str(other), str(self.english))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(other_record.read_bytes(), saved, 'A bad selected pair prevents all writes')

    def test_missing_and_orphaned_artifacts_fail(self):
        self.write_record()
        for path in (self.english, self.chinese, self.record):
            with self.subTest(path=path.name):
                saved = path.read_bytes()
                path.unlink()
                self.assertTrue(check_directory(self.root / 'lessons'))
                path.write_bytes(saved)
        self.english.unlink()
        self.chinese.unlink()
        self.assertTrue(check_directory(self.root / 'lessons'), 'Orphaned YAML must be reported')

    def test_malformed_record_and_out_of_scope_path_fail(self):
        self.write_record()
        self.record.write_text('sections: [not a confirmed record]\n')
        self.assertNotEqual(self.command().returncode, 0)
        self.assertNotEqual(self.command('--write', str(self.root / 'outside.md')).returncode, 0)

    def test_hashes_cover_fenced_headings_and_comments(self):
        en = self.english.read_text(encoding='utf-8')
        zh = self.chinese.read_text(encoding='utf-8')
        block = '```text\n## Example heading\n```\n<!--\n## hidden heading\n-->\n'
        original = record_text(en, zh)
        modified = record_text(en.replace('## Method', block + '\n## Method'),
                               zh.replace('## 方法', block + '\n## 方法'))
        self.assertNotEqual(original, modified)
        self.assertEqual(modified.count('    en:'), 5)
        self.assertEqual(original, record_text(en.replace('\n', '\r\n'), zh.replace('\n', '\r\n')))

    def test_confirmation_does_not_prove_translation(self):
        self.write_record()
        self.change(self.english, '## Lesson', 'This sentence has no Chinese counterpart.\n\n## Lesson')
        self.assertNotEqual(self.command().returncode, 0)
        # A mistaken human confirmation can pass: hashes deliberately cannot judge meaning.
        self.write_record()
        self.assertEqual(self.command().returncode, 0)


if __name__ == '__main__':
    unittest.main()
