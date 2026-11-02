"""Check lesson pairs and their explicitly confirmed section hashes.

Supports unindented/three-space-indented fences and single-line backtick spans.
This is not a general CommonMark parser or a translation quality checker.
"""

import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re

from check_lessons import EN_SECTIONS, LEGACY_SECTIONS, SECTIONS, prose, validate

ROOT = Path(__file__).resolve().parents[1]
SECTION_KEYS = ('intro', 'problem', 'lesson', 'method', 'case')


def signature(text):
    blocks, spans, errors = [], {}, []
    section = 0
    fence = None
    content = []
    info = ""
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                blocks.append((section, info, "\n".join(content)))
                fence = None
            else:
                content.append(line)
            continue
        if marker:
            fence, info, content = marker[1], marker[2].strip(), []
            continue
        if line.startswith("## "):
            section += 1
        # Count exact literals per H2 section; translated prose may reorder them.
        tokens = list(re.finditer(r"`+", line))
        index = 0
        while index < len(tokens):
            opening = tokens[index]
            closing = next((j for j in range(index + 1, len(tokens))
                            if tokens[j][0] == opening[0]), None)
            if closing is None:
                errors.append(f"line {number}: unmatched backticks; use single-line code spans")
                break
            value = line[opening.end():tokens[closing].start()]
            spans.setdefault(section, Counter())[value] += 1
            index = closing + 1
    if fence:
        errors.append("unclosed code fence")
    return blocks, spans, errors


def validate_pair(english, chinese):
    en_blocks, en_spans, en_errors = signature(english)
    zh_blocks, zh_spans, zh_errors = signature(chinese)
    errors = ["English: " + e for e in en_errors] + ["Chinese: " + e for e in zh_errors]
    if en_blocks != zh_blocks:
        errors.append("fenced code differs: compare section, language, order, and content")
    for section in sorted(en_spans.keys() | zh_spans.keys()):
        en, zh = en_spans.get(section, Counter()), zh_spans.get(section, Counter())
        if en != zh:
            errors.append(f"section {section}: inline code differs; English-only {dict(en - zh)!r}; Chinese-only {dict(zh - en)!r}")
    return errors


def section_texts(text):
    """Split the fixed lesson sections, preserving all text except CRLF spelling."""
    text = text.replace('\r\n', '\n')
    # Mask comments without shifting offsets; retain them in the hashed content.
    masked = re.sub(r'<!--.*?-->', lambda m: re.sub(r'[^\n]', ' ', m[0]), text, flags=re.S)
    starts, offset, fence = [0], 0, None
    for line in masked.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\n'))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        elif line.startswith('## '):
            starts.append(offset)
        offset += len(line)
    if len(starts) != len(SECTION_KEYS):
        raise ValueError('Expected four lesson sections before recording hashes.')
    return {key: text[start:end] for key, start, end in zip(SECTION_KEYS, starts, starts[1:] + [len(text)])}


def record_text(english, chinese):
    """Emit the complete canonical YAML; checking compares it without parsing YAML."""
    en, zh = section_texts(english), section_texts(chinese)
    lines = ['version: 1', 'sections:']
    for key in SECTION_KEYS:
        lines.append(f'  {key}:')
        for language, sections in (('en', en), ('zh', zh)):
            digest = hashlib.sha256(sections[key].encode('utf-8')).hexdigest()
            lines.append(f'    {language}: "{digest}"')
    return '\n'.join(lines) + '\n'


def english_path(path):
    for suffix in ('.i18n.yaml', '.zh.md', '.md'):
        if path.name.endswith(suffix):
            return path.with_name(path.name[:-len(suffix)] + '.md')
    raise ValueError(f'Expected a lesson .md, .zh.md or .i18n.yaml path: {path}')


def pair_paths(path):
    english = english_path(path)
    return english, english.with_name(english.stem + '.zh.md'), english.with_suffix('.i18n.yaml')


def inspect_pair(path, check_record=True):
    english, chinese, record = pair_paths(path)
    errors = []
    for language, file in (('English', english), ('Chinese', chinese)):
        if not file.is_file():
            errors.append(f'missing {language} counterpart: {file.name}')
    if errors:
        return errors, None
    en, zh = (file.read_text(encoding='utf-8') for file in (english, chinese))
    for language, text, expected in (('English', en, (EN_SECTIONS,)),
                                      ('Chinese', zh, (SECTIONS, LEGACY_SECTIONS))):
        errors.extend(f'{language}: {error}' for error in validate(text))
        headings = tuple(re.findall(r'^## (.+)$', prose(text), re.M))
        if headings not in expected:
            errors.append(f'{language}: lesson headings do not match the file language')
    for text, switcher in ((en, f'English | [中文]({chinese.name})'),
                           (zh, f'[English]({english.name}) | 中文')):
        if switcher not in prose(text).splitlines():
            errors.append(f'missing language switcher: {switcher}')
    errors.extend(validate_pair(en, zh))
    if errors:
        return errors, None
    expected = record_text(en, zh)
    if check_record:
        if not record.is_file():
            errors.append(f'missing consistency record: {record.name}')
        else:
            actual = record.read_text(encoding='utf-8')
            if actual != expected:
                blocks = re.findall(r'  (\w+):\n    en: "[a-f0-9]+"\n    zh: "[a-f0-9]+"\n', expected)
                changed = [key for key in blocks if re.search(
                    r'  ' + key + r':\n    en: "[a-f0-9]+"\n    zh: "[a-f0-9]+"\n', expected)[0] not in actual]
                detail = ', '.join(changed) or 'record format'
                errors.append(f'{record.name}: stale or invalid record ({detail}); review both languages, then use --write {english.as_posix()}')
    return errors, expected


def check_directory(directory):
    pairs = {english_path(path) for pattern in ('*.md', '*.i18n.yaml') for path in directory.rglob(pattern)}
    if not pairs:
        return ['No lesson pairs found.']
    return [f'{path.name}: {error}' for path in sorted(pairs) for error in inspect_pair(path)[0]]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pairs', nargs='*', help='Explicit lesson paths; either language or its record')
    parser.add_argument('--write', action='store_true', help='Record only named pairs after reviewing semantic consistency')
    args = parser.parse_args(argv)
    directory = (ROOT / 'lessons').resolve()
    if args.write and not args.pairs:
        parser.error('--write requires explicit reviewed lesson paths; there is no bulk-write default')
    try:
        selected = set()
        for value in args.pairs:
            path = Path(value).resolve()
            path.relative_to(directory)
            selected.add(english_path(path))
        if not args.pairs:
            errors = check_directory(directory)
        else:
            errors, pending = [], []
            for path in sorted(selected):
                pair_errors, record = inspect_pair(path, check_record=not args.write)
                errors.extend(f'{path.name}: {error}' for error in pair_errors)
                pending.append((pair_paths(path)[2], record))
            # Validate every selected pair before changing any record.
            if args.write and not errors:
                for path, text in pending:
                    with path.open('w', encoding='utf-8', newline='\n') as stream:
                        stream.write(text)
                    print(f'Recorded {path.relative_to(ROOT)}')
    except (OSError, UnicodeError, ValueError) as error:
        errors = [str(error)]
    for error in errors:
        print(error)
    print(f'Lesson pairing: {len(errors)} error(s). Hashes record confirmation, not translation correctness.')
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
