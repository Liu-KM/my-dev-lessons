# Consistency maintenance for English–Chinese documentation

English | [中文](bilingual-consistency-records.zh.md)

## Problem

Having two documents does not mean that both languages continue to express the same content. After one side changes, the other may remain unchanged. Links between them help readers switch languages but cannot detect missed updates.

Recording whole-file hashes (values used to detect content changes) creates another problem: two branches editing different sections still change the same record lines, causing unnecessary merge conflicts.

## Lesson

Maintain a bilingual pair as one unit and record hashes of both sides when their consistency is confirmed. After changes, review the counterpart and update the record; CI checks that the contents still match it. When parallel editing is common, record stable section identifiers to reduce conflicts between unrelated section edits.

## Method

Keep English `foo.md`, Chinese `foo.zh.md`, and a consistency record `foo.i18n.yaml` in the same directory. File names identify the pair, document links support language switching, and YAML stores the confirmed content hashes; it does not store the translations.

1. When either side changes, update the counterpart against the diff and use the terminology table to keep concepts consistent.
2. Compare corresponding sections, lists, code blocks, and other structures. After confirming semantic consistency, regenerate the record with a tool.
3. Review both languages and the record in the same PR. CI checks pair completeness, matching structure, and whether current hashes match the record.
4. For section-level records, use stable heading paths as keys. Editing one section should change only its entries, avoiding conflicts caused by a shared pair of whole-file hashes.

CI does not require the English and Chinese hashes to equal each other. It checks each side against its previously confirmed content. Regenerating the record can also make a bad translation pass hash checks, so a passing check cannot replace translation review.

This approach suits documents whose bilingual versions need ongoing maintenance. Choose record granularity to suit editing patterns; YAML alone enforces nothing without generation and checking tools.

## Case

[DSH commit `e7def469e1`: key translation pairing records by heading section](https://github.com/deepseek-ai/deepseek-harness/commit/e7def469e1390891cc45f78bea4063009abf6edd)

- **Problem or design goal**: Whole-file hashes made changes to different sections compete for the same record lines; a local merge driver could not resolve GitHub's mergeability checks.
- **Solution**: Identify corresponding sections by English heading-slug paths and store separate English and Chinese content hashes. Code fences and generated regions are checked separately and excluded from section hashes, avoiding unnecessary translation confirmation when shared code or generated content changes.
- **Evidence to inspect**: [Record implementation in the commit](https://github.com/deepseek-ai/deepseek-harness/blob/e7def469e1390891cc45f78bea4063009abf6edd/scripts/translation-pairing-record.ts); [bilingual maintenance rules at the inspected revision](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/docs/i18n/README.md). The latter describes three-file pairs, equal authority for both languages, structural checks, and confirmation.

Verification status: We read DSH's bilingual maintenance rules, section-record decision, YAML examples, and introducing commit; we have not reproduced its generator or conflict statistics. This project implemented a smaller checker for fixed-section lessons, with 19 local tests covering missing pairs, changed prose, shared code, explicit recording, and verification limits. Updating the PR collaboration lesson to reflect the completed PR #1 failed the check after an English-only edit and again after the Chinese update; recording the reviewed pair then passed and changed only the two case-section hashes. The CI configuration includes the read-only check; remote execution evidence belongs in the corresponding PR's checks.

Our records also include code and comments and use fixed section keys rather than DSH's general heading paths. The workflow and human-review responsibilities are defined in [bilingual lesson maintenance](../docs/bilingual-maintenance.md).
