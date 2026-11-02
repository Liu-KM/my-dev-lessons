"""Exercise rejection paths against the first real lesson."""

import re
import unittest

from check_lessons import ROOT, validate


class LessonChecks(unittest.TestCase):
    def setUp(self):
        self.sample = (ROOT / "lessons/docs-example-typecheck.md").read_text(encoding="utf-8")

    def test_real_sample(self):
        self.assertEqual(validate(self.sample), [])

    def test_missing_section(self):
        self.assertTrue(validate(self.sample.replace("## 经验结论", "### 经验结论")))

    def test_empty_section(self):
        text = re.sub(r"(## 经验结论\n).*?(\n## )", r"\1\n\2", self.sample, flags=re.S)
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
