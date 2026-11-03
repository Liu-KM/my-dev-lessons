# Issue 与 PR 协作规范

[English](pull-requests.md) | 中文

## 范围与追踪

独立改动拆分；完成同一结果所需的文档、实现、测试和 CI 一起审阅。Issue 记录问题、范围与验收条件；PR 提交具体方案。一个 Issue 可以对应多个 PR，不要求每次修改或聊天新建 Issue。

每个准备好审阅的 PR 必须关联至少一个本仓库 Issue。在正文单独写一行 `Refs #N` 表示关联，或 `Fixes #N` 表示解决；替换示例编号。PR 编号、代码块、引用和注释中的引用不算。Draft 可以暂缺信息，转为 ready 后必须补齐。

## 提交与合入

先在工作区完成改动、相关本地检查和下述协作审阅，用本地 PR 总结交给用户。用户审阅并授权后，才能提交、推送功能分支和创建远程 PR；提交前的总结不是已经发布的 PR。每个 commit 围绕一个逻辑完整的改动，不因检查通过就自动提交或推送。

获准发布后，尚在打磨的方案使用 Draft PR。范围、描述和验证证据齐备后再转为 ready；后续修正在同一分支推进，描述反映最终方案。远程必要检查必须在待合入的最新提交上通过；合入前重新核对检查、未解决的审阅意见及最终 diff，由用户明确确认后合入。CI 未运行、失败或结果属于旧提交时不能合入，绿色结果也不自动授权合入。

合并方式随改动决定：可将同一成果的零散进展 squash，或保留有意义的分步提交；不要为减少提交数合并独立问题。原理与案例见 [Git 提交与 PR 协作](../lessons/commits-and-pr-integration.zh.md)。

### 提交前协作审阅

Agent 准备改动时，默认完成以下流程后再交给用户审阅；正常的检查、协作与修正连续进行，不逐项请求确认。

常规审阅的子 Agent 默认使用 `gpt-6.1-sol`，推理强度为 `medium`。根据具体审阅发现定向交互；需要调整模型或强度时说明原因。

1. **作者准备**：完成本次改动、相关本地检查和 PR 描述草稿，确定审阅基线及文件范围，包括未跟踪的新文件。
2. **独立审阅**：请求一个未参与编写的 Agent 只读审阅。提供需求、基线、改动位置、来源和验证记录；审阅者自行读取 diff、相关文件及证据，不只检查作者的摘要。核对需求覆盖、细节和来源支持，并按[学习与采用](documentation.zh.md#学习与采用)判断与 DSH 的差异是否有充分依据；报告问题位置、依据、影响与未验证项。
3. **修正与复查**：作者处理发现，必要时请原审阅者定向复查受影响部分。无法消除的分歧、需要改变需求的选择及未完成的验证保留给用户判断，不为得到通过结论反复重审。
4. **用户审阅**：一次性提供可查看的改动与简短说明：完成了什么、双方看过哪些文件和来源、DSH 如何处理而本项目如何采用及为何不同、检查结果、发现及处理情况、待决定事项。本地给用户的总结只维护一份中文稿；英文发布正文可作为内部材料，避免维护多份用户审阅稿。

此流程是本项目的协作选择，不声称 DSH 使用完全相同的提交前流程，也不由 CI 自动触发。独立 Agent 不可用时如实说明缺口，不能把作者自查称为独立审阅。审阅通过不授权提交、推送或合入；用户授权仍按本节执行。后续修改只复查受影响的内容和检查。

## 分类

每个 PR 选择一个主要 `kind/*`，以及至少一个实质影响的 `area/*`。分类清单见 [pr-labels.json](../.github/pr-labels.json)。

| 类型 | 意图 |
| --- | --- |
| `kind/feature` | 新增或有意改变行为 |
| `kind/bug-fix` | 修正错误行为 |
| `kind/doc` | 以文档改动为主 |
| `kind/testing` | 测试或测试设施改动，不改变产品行为 |
| `kind/cleanup` | 不改变行为的维护 |
| `kind/dependency` | 无其他主要意图的依赖更新 |

初始领域为 `area/lessons`、`area/docs`、`area/ci`、`area/workflow`，分别表示经验案例、项目文档、自动检查、开发协作。配套测试不把功能 PR 变成测试 PR；文件被顺带修改也不要求增加其领域标签。新增领域时，在同一 PR 更新分类清单及含义。

## 描述与验证

使用 [PR 模板](../.github/pull_request_template.md)，固定标题为 `Motivation`、`Changes`、`Testing`，正文可用中文。说明问题、最终接口及行为变化、逐项验收方法；范围变化后更新描述。只将实际执行的检查列为通过，区分本地与 CI；未执行项明确说明。回归检查应证明错误样本失败、修复后通过。

AI 分阶段评级、百分比和徽章待定，不是必填项；可保留真实、简短的分工说明。CI 不能判断需求是否合理、分类是否准确或证据是否充分，仍需内容审阅和用户确认后合入。

## 并行与依赖 PR

互不依赖的工作各自从主线创建分支及独立 worktree。只有依赖另一 PR 的改动才建立 stack：子 PR 的 base 指向父 PR 分支，描述及验收只覆盖这一层。修复放在引入问题的 PR，再向后传播；每层分别验证。

同仓库的依赖链在 ready 前使用 GitHub 原生 stack。首次使用时确认 GitHub 功能和官方 CLI 扩展可用；不要把分支依赖关系当成已建立 stack。现有同作者 PR 可用 `gh stack link --base main <bottom-pr> <next-pr>` 关联，并复查服务端成员与顺序；不同作者先协调确认。不要自动拆除、重排现有 stack。

同步可用 merge-forward 或 `gh stack sync`；后者可能级联 rebase 并推送，必须检查每层变化、重新验证与审阅。重写使用 lease 保护，禁止裸 `--force`。合入前获取最新检查和审阅状态，经用户明确确认后用 `gh stack merge` 按确认范围合入。CI 不自动创建 stack、重写分支或合并。

原生 stack 不可用或涉及跨 fork 依赖时，不把手工逐个合并伪装成同等机制；保留草稿并决定替代流程。独立并行 PR 不受此限制。

## 自动检查与启用

[PR policy](../.github/workflows/pr-policy.yml) 从默认分支运行只读代码，获取最新 PR 元数据，检查非空章节、Issue 真实性、标签及非主线 base 的原生 stack 关系。它不执行 PR 分支代码。检查失去 API 权限或无法读取 stack 时失败，不静默跳过。修改 stack 元数据后，可手动触发并提供 PR 编号重新检查。

[标签初始化工作流](../.github/workflows/pr-labels.yml)由维护者手动运行，只补齐清单中缺失的标签，不删除或改写现有标签。规范文件和自动检查须一起审阅。

### 首次启用

首次引入检查器时，默认分支尚无该文件，不能要求引入它的 PR 已经运行新策略。按以下顺序操作，并在实际执行时记录结果和运行链接：

1. **合入前**：运行 `python scripts/check_lessons.py` 和 `python -m unittest discover -s scripts -p 'test_*.py'`，并检查本 PR 的文档 CI。人工核对 Issue、标签选择、描述和依赖关系；尚未创建的标签先记录拟用名称。通过审阅并获得用户合入确认后，才能合入。
2. **初始化**：在默认分支运行 `Initialize PR labels`，核对标签名称和含义，再为仍开放的 PR 补全标签。确认 `PR policy` 已出现在 Actions 中。
3. **首次实际运行**：选择下一次真实开发的开放 PR，补齐元数据并转为 ready，检查 `PR policy` 是否自动运行并针对该 PR 给出结果。记录 PR、head SHA、运行链接和结论。手动运行时填写 `pr_number`；手动运行成功只用于诊断，不能替代确认检查已出现在 PR 上。Draft 或已关闭 PR 会跳过，不能用其绿色结果证明策略已经验证。
4. **合入约束**：确认 PR 上实际出现的 `Issue, labels and stack` 与 `Documentation checks` 后，再将它们配置为必要检查，并核对适用分支、绕过权限和失败时的合入限制。未完成配置前，不能声称 GitHub 已强制执行规范。
5. **依赖 PR**：首次使用原生 stack 时，核对服务端成员顺序、父子分支和每层检查。仅修改 stack 元数据后可手动诊断；合入前仍要核对 PR 上的有效检查。独立 PR 通过不能证明 stack 路径已验证。

未完成启用验证时，相关 Issue 保持开放，PR 使用 `Refs #N`；完成实际验证后再记录结果并关闭。不要为演示失败制造无意义的 Issue 或 PR；失败样例由本地测试覆盖，远程触发与权限在真实工作中核验。

### 验证范围

本地测试覆盖正常与失败的元数据、PR 事件和手动输入入口、读取最新 PR、Draft/已关闭跳过、Issue 不存在、权限错误、网络失败，以及依赖 PR 的父节点和 stack 查询。HTTP 响应使用模拟数据；这些测试不证明 GitHub Actions 权限、事件触发或分支保护已经生效。

实际启用记录放在对应 PR 的验证说明中，分别列出本地测试、远程运行、标签、分支保护和 stack 实践的状态；尚未执行的项目明确标为未验证。

## 来源

- [DSH 协作规则](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/AGENTS.md)：独立改动拆分与修复归属。
- [DSH 标签设计](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/.agents/notes/implemented/process/2026-08-08-unified-github-label-taxonomy.md)：意图与影响领域分开。
- [DSH PR 描述规范](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/.agents/skills/dsh-pr-description/SKILL.md)：变化与验证对应；本项目暂不采用 AI 量化声明。
- [GitHub 原生 stack](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests)与[CLI 命令](https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands)：依赖链管理。
- [GitHub 工作流事件](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target)与[PR GraphQL 字段](https://docs.github.com/en/graphql/reference/pulls#pullrequeststack)：检查器的执行上下文与 stack 查询依据。

本项目的 Draft 暂缓检查、分类清单和只读工作流是具体实现选择，不声称完整复制 DSH 的策略系统。
