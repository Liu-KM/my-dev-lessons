# 让文档示例参与类型检查

## 问题与原因

文档中的 API 示例也是代码，但常规 CI 通常只编译指定的源码与测试文件，不会自动提取 Markdown 中的代码块。接口变化后，源码里的调用可能已经修好，文档中的示例却继续使用旧接口。

“修改代码时记得更新文档”依赖修改者找到所有相关示例。文档越分散，这种遗漏越难仅靠记忆避免。

## 经验结论

把依赖项目 API 的可编译文档示例纳入类型检查，并在 CI 中持续执行，让接口不兼容变成可定位的检查失败。

## 具体方法与边界

1. 从 Markdown 提取明确标记的代码示例，用项目当前的包与类型进行检查。
2. 将错误位置映射回文档，让开发者知道需要检查哪段示例。
3. 本地与 CI 使用同一个检查入口，避免两套检查逻辑各自变化。
4. 局部示例补充必要的 imports 和辅助声明；纯示意代码显式跳过，审查时判断是否合理。

优先覆盖读者会复制使用、依赖项目 API 的示例。这里的类型检查不生成发布产物，也不自动修正文档。它验证的是类型兼容性；需要验证运行行为时，还应执行示例或测试。文字解释和推荐写法仍需审查。

## 参考案例与验证状态

2026 年 6 月 11 日，DSH 的 review 发现 echo-agent README 中的 `registerAdapter([])` 描述与实际示例不符，另一处工具示例使用 `args: any`，没有采用项目已有的 `defineTool` 类型推导方式。项目虽然要求文档同步，仍出现了文档偏差。[原始修复](https://github.com/deepseek-ai/deepseek-harness/commit/2b447625fa0d7d04aa97095dbb2fa42e82f3aa9b)

6 月 14 日，DSH 加入 `doc-typecheck`：提取 Markdown 中的 `ts` 代码块，用 `tsc --noEmit` 检查，并通过同一个 `doc-sync` 命令接入本地 pre-push 和 CI。[决策记录](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/docs/adr/0014-doc-sync-enforcement.md) · [检查脚本](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/scripts/doc-typecheck.ts) · [CI 接入提交](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

这个方案没有覆盖最初 review 发现的全部问题：表格中的行内代码不在提取范围内，显式 `any` 也未必引起类型错误。它增加了可编译示例的兼容性检查，不能据此认定所有文档偏差都被解决。

验证状态：已阅读 DSH 的历史修复、决策记录和检查实现，未运行历史检查或测量其效果。本项目尚未实施文档示例类型检查；当前文档 CI 验证格式、链接和经验结构。
