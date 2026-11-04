# 文档代码示例类型检查

[English](docs-example-typecheck.md) | 中文

## 问题

文档中的 API 示例也是代码，但常规 CI 通常只编译指定的源码与测试文件，不会自动提取 Markdown 中的代码块。接口变化后，源码里的调用可能已经修好，文档中的示例却继续使用旧接口。

“修改代码时记得更新文档”依赖修改者找到所有相关示例。文档越分散，这种遗漏越难仅靠记忆避免。

## 经验

把依赖项目 API 的可编译文档示例纳入类型检查，并在 CI 中持续执行，在示例与当前 API 不兼容时报告对应的文档位置。

## 方法

1. 从 Markdown 提取明确标记的代码示例，用项目当前的包与类型进行检查。
2. 将错误位置映射回文档，让开发者知道需要检查哪段示例。
3. 本地与 CI 调用同一个检查脚本，避免两套检查逻辑各自变化。
4. 为省略了上下文的示例补充必要的导入和辅助声明；纯示意代码需明确标记为跳过检查，并由审阅者确认跳过的理由。

优先覆盖读者会复制使用、依赖项目 API 的示例。这里的类型检查不生成发布产物，也不自动修正文档。它验证的是类型兼容性；需要验证运行行为时，还应执行示例或测试。文字解释和推荐写法仍需审查。

## 案例

[DSH 提交 `204c36ed76`：将文档示例类型检查和事件表检查接入 CI](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

- **解决的问题**：文档中的 TypeScript 示例未纳入类型检查，API 变化引起的示例不兼容需要依靠人工审查发现。
- **采取的办法**：新增 `doc-typecheck`，提取 Markdown 中的 `ts` 代码块，用 `tsc --noEmit` 检查；补充示例所需的 imports 和辅助声明，并通过 `doc-sync` 接入本地 pre-push 和 CI。
- **可查看的证据**：[检查脚本](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/scripts/doc-typecheck.ts)给出提取、编译和报错机制；[决策记录](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/docs/adr/0014-doc-sync-enforcement.md)说明适用范围与取舍。

关联案例：[提交 `2b447625fa`](https://github.com/deepseek-ai/deepseek-harness/commit/2b447625fa0d7d04aa97095dbb2fa42e82f3aa9b)修正了 README 中错误的 `registerAdapter([])` 描述，并把工具示例的 `args: any` 改为 `defineTool` 类型推导。这两处错误也说明了检查会遗漏什么：表格行内代码不属于提取范围，显式 `any` 未必引起类型错误，仍需要审查。

验证状态：已阅读 DSH 的历史修复、决策记录和检查实现，未运行历史检查或测量其效果。本项目尚未实施文档示例类型检查；双语一致性检查也不验证示例类型。
