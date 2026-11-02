# 让文档示例参与类型检查

当文档中的代码用于教读者调用项目 API 时，应把可编译的示例纳入类型检查。这样，接口变化导致示例不兼容时，可以由检查程序提示，而不只依赖修改者记得同步文档。

## DSH 的具体案例

2026 年 6 月 11 日，DSH 修正了两处文档：echo-agent README 中的 `registerAdapter([])` 描述与实际注册 `mock-echo` 的示例不符；工具开发示例仍使用 `args: any`，修复后改为通过 `defineTool` 推导参数类型。这说明文档虽然已有同步要求，仍会偏离实现或推荐用法。

随后，DSH 在 6 月 14 日引入 `doc-typecheck`，将文档中可编译的 TypeScript 示例纳入自动检查。

## DSH 的解法

1. 从指定范围的 Markdown 中提取 `ts` 代码块，写入临时 TypeScript 文件。
2. 使用仓库当前的包与类型解析配置，执行 `tsc --noEmit`，检查示例是否与当前 API 类型兼容。
3. 检查失败时，将错误位置映射回原始文档，便于修改。
4. 将检查接入 `doc-sync` 命令，本地 pre-push 与 CI 调用同一个入口。

局部示例补充必要的 imports 和辅助声明；纯示意代码可显式标记为 `ts ignore-check`。这让可检查的示例得到验证，也保留了文档省略无关实现的能力。

这里的“编译”是静态类型检查，不生成发布产物。CI 负责持续验证；CD 的部署步骤不是这条经验的重点。检查发现不一致后仍需修改代码或文档，并不会自动将两者对齐。

## 适用范围与边界

优先用于读者会复制使用、依赖项目 API 的代码示例。API 变化频繁、示例分散时，这类检查尤其值得考虑。其他语言可采用相应的编译、类型检查或示例测试机制，具体选择取决于需要验证的承诺。

检查通过只说明示例满足所检查的类型约束，不保证示例可独立运行、行为正确或写法值得推荐。DSH 最初修正的表格行内调用不在 `ts` 代码块提取范围内，显式 `any` 也未必引起类型错误；因此，这项检查没有覆盖最初 review 发现的全部问题。

## 来源与本项目状态

- [文档偏差的修复，2026-06-11](https://github.com/deepseek-ai/deepseek-harness/commit/2b447625fa0d7d04aa97095dbb2fa42e82f3aa9b)
- [文档同步检查的决策记录，2026-06-14](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/docs/adr/0014-doc-sync-enforcement.md)
- [当时的检查脚本](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/scripts/doc-typecheck.ts)
- [接入 pre-push 和 CI 的提交](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

本项目已讨论确认保留这条经验，依据为 DSH 的历史代码与决策记录。尚未运行历史检查或在本项目实现同类检查；记录这条经验不表示本仓库已经配置文档编译 CI。
