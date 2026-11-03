"""Run the repository's Python documentation checks from one shared entry."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# The command list lives here; documentation and CI invoke this file.
CHECKS = (
    ('scripts/check_doc_entry.py',),
    ('scripts/check_lessons.py',),
    ('scripts/check_lesson_pairs.py',),
    ('scripts/check_doc_budgets.py',),
    ('-m', 'unittest', 'discover', '-s', 'scripts', '-p', 'test_*.py'),
)


def main():
    for args in CHECKS:
        print('Running: python ' + ' '.join(args), flush=True)
        result = subprocess.run([sys.executable, *args], cwd=ROOT)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
