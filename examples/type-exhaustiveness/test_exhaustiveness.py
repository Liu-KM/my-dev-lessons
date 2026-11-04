"""Exercise actual static diagnostics and observable classification behavior."""

from collections import Counter
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

import report
import kernel_report
from open_events import route_event

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "mypy.ini"


def check_source(source):
    with tempfile.TemporaryDirectory(prefix="exhaustiveness-") as directory:
        path = Path(directory) / "candidate.py"
        path.write_text(source, encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-m", "mypy", "--config-file", str(CONFIG),
             "--no-incremental", "--cache-dir", str(Path(directory) / "cache"),
             "--show-error-codes", str(path)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            check=False,
        )


class ExhaustivenessTests(unittest.TestCase):
    def test_wide_default_typechecks_but_misclassifies_cancellation(self):
        path = ROOT / "fixtures" / "wide_default.py"
        checked = check_source(path.read_text(encoding="utf-8"))
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        legacy = runpy.run_path(str(path))
        observed = Counter(legacy["classify"](reason)
                           for reason in ("eos", "max_tokens", "cancelled"))
        self.assertEqual(dict(observed), {"generated": 1, "length_limit": 2})
        self.assertNotEqual(observed.get("cancelled", 0), 1)

    def test_only_adding_a_variant_breaks_the_protected_baseline(self):
        before = (ROOT / "fixtures" / "closed_before.py").read_text(encoding="utf-8")
        old = 'FinishReason = Literal["eos", "max_tokens"]'
        self.assertEqual(before.count(old), 1)
        checked = check_source(before)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        changed = before.replace(old, 'FinishReason = Literal["eos", "max_tokens", "cancelled"]')
        checked = check_source(changed)
        self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
        self.assertIn('Argument 1 to "assert_never"', checked.stdout)
        self.assertIn("cancelled", checked.stdout)
        self.assertIn("[arg-type]", checked.stdout)
        print("Expected omission diagnostic:", checked.stdout.strip())

    def test_repaired_report_typechecks(self):
        checked = check_source((ROOT / "report.py").read_text(encoding="utf-8"))
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_all_categories_have_the_required_meaning(self):
        self.assertEqual(report.classify("eos"), "generated")
        self.assertEqual(report.classify("max_tokens"), "length_limit")
        self.assertEqual(report.classify("cancelled"), "cancelled")
        self.assertEqual(
            report.summarize(["eos", "eos", "max_tokens", "cancelled"]),
            {"generated": 2, "length_limit": 1, "cancelled": 1},
        )

    def test_invalid_runtime_value_fails_instead_of_becoming_a_known_category(self):
        with self.assertRaises(AssertionError):
            report.classify("rogue")

    def test_open_events_delegate_to_the_extension_owner(self):
        received = []

        def extension(kind):
            received.append(kind)
            return "extension:" + kind

        self.assertEqual(route_event("measurement", extension), "built-in measurement")
        self.assertEqual(received, [])
        self.assertEqual(route_event("plugin:trace", extension), "extension:plugin:trace")
        self.assertEqual(received, ["plugin:trace"])


class TransferReplayTests(unittest.TestCase):
    def test_kernel_before_typechecks_but_counts_unsupported_as_passed(self):
        path = ROOT / "fixtures" / "kernel_before.py"
        checked = check_source(path.read_text(encoding="utf-8"))
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        old = runpy.run_path(str(path))
        self.assertEqual(
            old["summarize"](["ok", "unsupported", "error", "ok"]),
            {"passed": 3, "failed": 1, "unsupported": 0},
        )

    def test_independent_repair_has_correct_meanings_and_typechecks(self):
        checked = check_source((ROOT / "kernel_report.py").read_text(encoding="utf-8"))
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        for value, expected in (("ok", "passed"), ("error", "failed"),
                                ("unsupported", "unsupported")):
            self.assertEqual(kernel_report.classify(value), expected)
        self.assertEqual(
            kernel_report.summarize(["ok", "unsupported", "error", "ok"]),
            {"passed": 2, "failed": 1, "unsupported": 1},
        )
        self.assertEqual(kernel_report.summarize([]),
                         {"passed": 0, "failed": 0, "unsupported": 0})
        self.assertEqual(kernel_report.summarize(iter(["unsupported"])),
                         {"passed": 0, "failed": 0, "unsupported": 1})

    def test_future_kernel_category_exposes_omission(self):
        source = (ROOT / "kernel_report.py").read_text(encoding="utf-8")
        old = 'Outcome = Literal["ok", "error", "unsupported"]'
        self.assertEqual(source.count(old), 1)
        checked = check_source(source.replace(
            old, 'Outcome = Literal["ok", "error", "unsupported", "timeout"]'))
        self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
        self.assertIn("timeout", checked.stdout)
        self.assertIn('Argument 1 to "assert_never"', checked.stdout)
        self.assertIn("[arg-type]", checked.stdout)


if __name__ == "__main__":
    unittest.main()
