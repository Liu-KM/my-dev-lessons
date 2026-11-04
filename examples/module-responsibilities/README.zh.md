# Attention 实现替换与公共校验

[English](README.md) | 中文

本例实践[将可替换实现与公共流程分开](../../lessons/module-responsibilities.zh.md)，验证代码职责与 dense causal self-attention 语义。

## 运行

在仓库根目录运行，Python 3.9 及以上：

```sh
python -m pip install -r examples/module-responsibilities/requirements.txt
python -m unittest discover -s examples/module-responsibilities -p 'test_*.py' -v
python examples/module-responsibilities/demo.py
```

NumPy 版本由依赖文件指定。CI 使用相同的安装和测试命令，执行结果见对应 PR 提交的检查记录。

## 职责

| 文件 | 负责什么 | 新增实现时怎样修改 |
| --- | --- | --- |
| [contract.py](contract.py) | 输入的形状、dtype 和非有限值检查 | 仅在共同要求改变时修改 |
| [kernels.py](kernels.py) | 全矩阵与 query 分块计算，各自保证全局 causal mask | 增加计算函数；共同实验流程不复制 |
| [experiment.py](experiment.py) | 调用前校验、计算计时、输出形状与 dtype 检查 | 通过函数参数接收实现，不导入具体 kernel |
| [demo.py](demo.py) | 输入生成、实现选择和结果比较 | 在这里接入第二种实现 |
| [test_attention.py](test_attention.py) | 独立参考值、错误对照及共同要求的验证 | 接入实现后参加相同检查 |

接口是计算函数接收 Q、K、V 并返回输出数组的约定，不是另一套服务。直接调用 kernel 属于内部计算路径；示例的公共入口是 `run_attention`。新增需要状态、异步执行或不同输入形状的实现时，应重新审查接口，不能假定本例已覆盖。

两种计算接收同一 float32 输入，形状为 [2,4,128,64]，seed=7，dropout=0。query 分块为 32，但每块读取完整 K/V；它仍然是 dense causal attention。两个实现分别对照逐 token 的 float64 参考计算，容差固定为 rtol=1e-5、atol=1e-6，再比较两者。计时只包围计算函数，排除输入生成和校验；没有预热与重复测量，不能据此声称加速。

## 可复跑的错误与修复

1. **原有检查**：[错误 mask](fixtures/block_local_mask.py)在只有 32 个 token 时通过参考值检查。
2. **新增场景**：保持该实现与容差不变，把输入增加为 128 个 token。它在每个块重置 query 位置，跨块后与独立参考值不一致。本地最大绝对误差为 3.389124662。
3. **修复**：当前分块实现使用全局 query 位置；两种实现均通过参考值检查。另以 Q/K 为零、V 为位置编号的输入验证第 i 行等于 0..i 的均值，覆盖 31/32、63/64 和最后一行；非整块输入也参与检查。
4. **公共要求的演进**：[旧校验](fixtures/validation_before.py)只检查形状与 dtype，放行含 NaN 的输入，导致两种算法返回 NaN。测试临时接回同一旧校验来复现；恢复当前共同校验后，两种算法均在执行前拒绝该输入，计算函数未分别加入新校验。

测试还覆盖 K/V 长度不匹配、输入不被修改和公共输出检查。错误对照只在测试中使用；它们展示为什么需要这些检查，不是 DSH 发生过 attention 故障的证据。

## 验证状态

本地 Python 3.9.7 / NumPy 2.0.0 下八项测试通过，demo 的两种输出最大绝对差约为 5.36e-7。未参与编写的 Sol / medium Agent 已核对实现、双语材料与 DSH 来源，并独立复跑八项测试及文档检查，未发现行为阻碍。DSH 的来源与采用差异见 lesson，远程执行结果见对应 PR 的检查记录。
