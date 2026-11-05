"""Check the small Markdown contract used by lessons/, not prose quality."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("问题", "经验", "方法", "案例")
EN_SECTIONS = ("Problem", "Lesson", "Method", "Case")
LEGACY_SECTIONS = ("问题与原因", "经验结论", "具体方法与边界", "参考案例与验证状态")


def prose(text):
    """Ignore fenced examples and HTML comments when checking document structure."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    result = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
        else:
            result.append(line)
    return "\n".join(result)


def validate(text):
    body = prose(text)
    errors = []
    titles = re.findall(r"^# (\S.*)$", body, re.M)
    if len(titles) != 1:
        errors.append("需要一个非空一级标题")
    headings = list(re.finditer(r"^## (.+)$", body, re.M))
    # Accept a complete old or new format during migration, never mixed headings.
    actual = tuple(match[1].strip() for match in headings)
    english = any(heading in EN_SECTIONS for heading in actual)
    legacy = any(heading in LEGACY_SECTIONS for heading in actual)
    expected = EN_SECTIONS if english else LEGACY_SECTIONS if legacy else SECTIONS
    if actual != expected:
        errors.append("二级章节须按顺序为：" + "、".join(expected))
    sections = {}
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        content = body[match.end():end].strip()
        sections[match[1].strip()] = content
        if not content:
            errors.append("章节不能为空：" + match[1])
    case = sections.get(expected[-1], "")
    if not re.search(r"\[[^\]\n]+\]\(https?://[^\s)]+\)", case):
        errors.append("参考案例需要至少一个带标签的 HTTP(S) 原始来源链接")
    if re.search(r"\{\{.*?\}\}", text, re.S):
        errors.append("请替换模板占位符 {{…}}")
    return errors


def main():
    files = sorted((ROOT / "lessons").rglob("*.md"))
    failures = 0
    for path in files:
        for error in validate(path.read_text(encoding="utf-8")):
            print(f"{path.relative_to(ROOT)}: {error}")
            failures += 1
    print(f"Checked {len(files)} lesson(s); {failures} error(s).")
    return 1 if failures or not files else 0


if __name__ == "__main__":
    raise SystemExit(main())
