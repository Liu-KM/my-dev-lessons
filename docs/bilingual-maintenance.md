# Bilingual lesson maintenance

English | [中文](bilingual-maintenance.zh.md)

This policy covers every Markdown file under `lessons/`. Each lesson has sibling English `foo.md`, Chinese `foo.zh.md`, and consistency-record `foo.i18n.yaml` files. Both documents link to their counterpart, and either language may be edited first.

## Editing and confirmation

1. Update the counterpart against the diff, preserving conclusions, conditions, sources, and verification limits. Change only the affected parts of an existing translation.
2. Review meaning paragraph by paragraph and follow the [terminology conventions](../TERMINOLOGY.md). Preserve commands, parameters, paths, and API identifiers verbatim; shared code must match. Do not remove necessary information merely to pass comparison.
3. After confirming consistency, explicitly record the selected lesson. The following command uses this project's bilingual-maintenance lesson as a real entry point; replace the path for a new lesson.

```sh
python scripts/check_lesson_pairs.py --write lessons/bilingual-consistency-records.md
```

4. Run the checks and review both languages and the record as one change.

```sh
python scripts/check_lesson_pairs.py
python scripts/check_lessons.py
python -m unittest discover -s scripts -p 'test_*.py'
```

The recording command accepts English, Chinese, or record paths, including an explicit list of reviewed lessons. It writes records only after every selected pair passes structure and code checks; `--write` without paths fails. The default check is read-only and does not confirm translations on the maintainer's behalf.

Start a new lesson from the [Chinese template](../templates/lesson.zh.md) or [English template](../templates/lesson.md), then add the counterpart, language links, and record. Rename all three files and repair inbound links together; delete all three when removing a lesson. Orphaned records also fail the check.

## Record format

Generate records with the script rather than editing them manually. The current format is fixed-layout YAML: `version: 1`, with `intro`, `problem`, `lesson`, `method`, and `case` under `sections`. Each entry stores separate `en` and `zh` SHA-256 hashes. The title and introduction belong to `intro`; deeper headings belong to their enclosing second-level section.

Hashes cover all text in each part, including code and comments; only CRLF line endings are normalized to LF. The two languages' hashes need not match each other: each is compared with its own last-confirmed content. Editing one section leaves the other sections' records unchanged. Format validation compares the full generated text; the tool does not provide a general YAML editing interface.

This project uses keys for its fixed four-section lessons. DSH uses general heading paths and separately excludes certain code and generated content. These are different tools and incompatible record formats; see [consistency maintenance for English–Chinese documentation](../lessons/bilingual-consistency-records.md) for the case.

## Check coverage

| Automated check | Human review still required |
| --- | --- |
| Both languages and the record exist; language links point to the pair | Conclusions, conditions, and evidence are equivalent |
| Both sides use their language's fixed lesson sections | Paragraphs, lists, and tables preserve meaning and ordering |
| Fenced code and inline code within each second-level section match | Terminology is appropriate and prose is natural |
| Current section contents match the confirmed record | Commands exist and behave as documented |

Even when both sides have changed, the check fails until the record is updated. A mistaken translation can pass after re-recording, so refreshing hashes cannot replace semantic review. CI runs the read-only check; configuration alone does not prove remote execution or a required status check.

README, project policies, templates, and the terminology table are outside the hash-check scope for now; existing bilingual pairs should still be maintained together. This scope does not require translations of local skills, the reference clone, or temporary drafts.
