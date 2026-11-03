"""Check standing-document ceilings; --list reports usage without enforcing it.

The manifest owns limits and explicit metrics. The documentation policy owns
scope and adjustment review. This checker never writes files or raises limits.
"""

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path('scripts/doc-budgets.manifest.json')


def count_units(text, metric):
    """Count whole-file whitespace words or non-whitespace Unicode characters."""
    if metric == 'words':
        return len(text.split())
    if metric == 'characters':
        return sum(not char.isspace() for char in text)
    raise ValueError(f'unknown metric: {metric!r}')


def inspect_budgets(root):
    manifest = json.loads((root / MANIFEST).read_text(encoding='utf-8'))
    if not isinstance(manifest, dict):
        raise ValueError('manifest must map file paths to metric/max entries')
    rows, errors = [], []
    for path, budget in manifest.items():
        if not isinstance(budget, dict):
            errors.append(f'{path}: expected a metric/max entry')
            continue
        metric, ceiling = budget.get('metric'), budget.get('max')
        if metric not in ('words', 'characters'):
            errors.append(f'{path}: metric must be words or characters')
            continue
        if type(ceiling) is not int or ceiling <= 0:
            errors.append(f'{path}: max must be a positive integer')
            continue
        target = root / path
        if not target.is_file():
            errors.append(f'{path}: budgeted file does not exist; update the manifest when moving it')
            continue
        actual = count_units(target.read_text(encoding='utf-8'), metric)
        rows.append(f'{"OVER" if actual > ceiling else "ok"}: {path}: {actual}/{ceiling} {metric}')
        if actual > ceiling:
            errors.append(f'{path}: {actual} {metric} exceeds {ceiling}; relocate or condense first, and justify any ceiling increase in the PR')
    return rows, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='report usage and entry errors without enforcing ceilings')
    args = parser.parse_args()
    try:
        rows, errors = inspect_budgets(ROOT)
    except (OSError, ValueError) as exc:
        print(f'Documentation budgets: {exc}', file=sys.stderr)
        return 1
    if args.list:
        print('\n'.join(rows + ['ERROR: ' + error for error in errors]))
        return 0
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Documentation budgets: {len(rows)} files within ceiling.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
