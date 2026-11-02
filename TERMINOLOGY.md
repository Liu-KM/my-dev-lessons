# 中英文术语约定

本表约定本项目中的概念与英文写法，不主张所有词在其他语境中一一对应。写作和翻译时按含义选择术语；只新增实际需要统一或容易混淆的词。

## 中文正文中的术语

双语文档不要求逐词翻译。借鉴 DSH 对缩写、保留英文的术语和中文译名的区分，本项目按实际使用约定如下；不直接继承 DSH 的全部词表。

| 中文正文写法 | 英文 | 使用约定 |
| --- | --- | --- |
| 哈希 | hash | 首次可写“哈希（hash，用于检测内容变化）”；不以“内容指纹”替代。本文档语境下不称 hashcode；引用具体 API 或方法名时保留原名。 |
| API、CI、PR | API、CI、PR | 保留通用缩写；需要解释时在首次出现处补充。PR 指 Pull Request。 |
| Markdown、YAML、TypeScript | Markdown、YAML、TypeScript | 保留格式或语言名称及其大小写。 |
| commit、push、merge、squash | commit、push、merge、squash | 指 Git 操作或合并方式时可保留英文；一般叙述仍可用“提交”“推送”“合入”“压缩提交”。命令原样保留。 |
| pre-push、doc-sync、doc-typecheck | pre-push、doc-sync、doc-typecheck | 保留 hook 或项目检查入口的原名，方便定位实现。 |
| slug | slug | 指用于路径或锚点的标题标识，首次使用时解释；不翻译代码中的标识符。 |

是否保留英文取决于通行用法和含义是否准确，不以英文越多越好。已有自然中文表达的“类型检查”“分支”“代码块”等继续使用中文。

## 经验与案例

| 中文 | 英文 | 含义与使用边界 |
| --- | --- | --- |
| 开发经验 | lesson learned；复数 lessons learned | 从具体开发经历中提炼的认识，包括成功做法与失败教训。强调总结出的认识；泛指个人开发经历或熟练程度时用 development experience，不使用本词条替代。项目标题可用 engineering lessons learned 明确工程语境。 |
| 案例 | case | 用于讨论的具体设计、实践或问题解决过程。 |
| 案例分析 | case study | 对案例的背景、决策、实现、结果与取舍进行分析；不把每个简短例子都称为 case study。 |
| 最佳实践 | best practice | 比单个案例中的有效做法更强的评价。总结 DSH 的做法时，优先称实践或经验，不因其被采用就称最佳实践。 |

## 文档检查与持续集成

| 中文 | 英文 | 含义与使用边界 |
| --- | --- | --- |
| 文档检查 | documentation checks | 本项目对类型、链接、一致性等具体检查的统称。此前讨论中的“文档验证”若未指定方法，按此宽泛含义理解；不宣称整份文档已经正确。 |
| 类型检查 | type checking | 检查代码是否满足类型约束；不等于执行测试或验证运行结果。 |
| 文档代码示例 | documentation code example | 文档中展示的代码。谈 Markdown 的语法单元时用“代码块”（code block）；代码块不一定是可运行示例。 |
| 持续集成 | continuous integration（CI） | 在集成变更的流程中自动执行构建、检查或测试。是否检查文档取决于具体配置。 |
| 持续交付 | continuous delivery（CD） | 自动准备可发布的变更，发布到生产环境可以保留人工决策。 |
| 持续部署 | continuous deployment（CD） | 将通过既定流程的变更自动部署到生产环境。CD 有两种常见展开方式，涉及具体流程时写清是哪一种。 |

“文档验证”没有在此固定为 validation 或 verification：两者在部分工程标准中有专门区分。描述脚本时优先写具体动作，例如 type checking、link checking 或 consistency checking，避免仅凭中文“验证”选择英文。

## 维护方式与参考

写作和翻译时参考本表；概念含义变化时，同步修改使用它的相关内容。术语表提供约定，不能自动保证文档一致，目前没有术语自动检查。

- [DSH 术语表](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/docs/i18n/terminology.md)：借鉴其明确默认写法与使用边界的方式；本表不直接继承 DSH 的专用词与翻译禁令。
- [NASA Lessons Learned](https://llis.nasa.gov/)：lessons learned 的工程知识整理用法参考；本项目不继承其审核或有效性标准。
- [TypeScript noEmit](https://www.typescriptlang.org/tsconfig/noEmit)：类型检查可以不生成输出文件。
