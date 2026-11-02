"""Exercise rejection paths against the first real lesson."""

import re
import unittest

from check_lessons import ROOT, SECTIONS, LEGACY_SECTIONS, EN_SECTIONS, validate


class LessonChecks(unittest.TestCase):
    def setUp(self):
        path = ROOT / "lessons/docs-example-typecheck.zh.md"
        if not path.exists():
            path = ROOT / "lessons/docs-example-typecheck.md"
        self.original = path.read_text(encoding="utf-8")
        self.sample = self.original
        for old, new in zip(LEGACY_SECTIONS, SECTIONS):
            self.sample = self.sample.replace('## ' + old + '\n', '## ' + new + '\n')

    def test_real_sample(self):
        self.assertEqual(validate(self.original), [])
        self.assertEqual(validate(self.sample), [])

    def test_legacy_format_and_mixed_heading_rejection(self):
        legacy = self.sample
        for new, old in zip(SECTIONS, LEGACY_SECTIONS):
            legacy = legacy.replace('## ' + new + '\n', '## ' + old + '\n')
        self.assertEqual(validate(legacy), [])
        self.assertTrue(validate(legacy.replace('## 经验结论\n', '## 经验\n')))

    def test_english_structure_and_rejection_paths(self):
        # Only the heading/status contract is translated; no other lesson is needed.
        english = self.sample
        for chinese_heading, english_heading in zip(SECTIONS, EN_SECTIONS):
            english = english.replace('## ' + chinese_heading + '\n', '## ' + english_heading + '\n')
        english = english.replace('验证状态：', 'Verification status: ')
        self.assertEqual(validate(english), [])
        self.assertTrue(validate(english.replace("## Lesson", "## 经验")))
        self.assertTrue(validate(re.sub(r"^Verification status:.*$", "", english, flags=re.M)))
        self.assertTrue(validate(re.sub(r"^Verification status:.*$", "Verification status: ", english, flags=re.M)))

    def test_missing_section(self):
        self.assertTrue(validate(self.sample.replace("## 经验", "### 经验")))

    def test_empty_section(self):
        text = re.sub(r"(## 经验\n).*?(\n## )", r"\1\n\2", self.sample, flags=re.S)
        self.assertTrue(any("不能为空" in error for error in validate(text)))

    def test_missing_sources(self):
        text = re.sub(r"\[[^\]]+\]\(https?://[^)]+\)", "来源已移除", self.sample)
        self.assertTrue(any("来源链接" in error for error in validate(text)))

    def test_missing_verification(self):
        text = re.sub(r"^验证状态：.*$", "", self.sample, flags=re.M)
        self.assertTrue(any("验证状态" in error for error in validate(text)))

    def test_fenced_text_cannot_supply_missing_verification(self):
        text = re.sub(r"^验证状态：.*$", "```text\n验证状态：示例\n```", self.sample, flags=re.M)
        self.assertTrue(any("验证状态" in error for error in validate(text)))

    def test_unfilled_template(self):
        template = (ROOT / "templates/lesson.md").read_text(encoding="utf-8")
        self.assertTrue(any("占位符" in error for error in validate(template)))


if __name__ == "__main__":
    unittest.main()
