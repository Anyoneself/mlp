# PyTorch FSDP

**阶段：** 分布式训练  
**建议时间：** 第 20 周前半段  
**前置条件：** 完成任务 37

## 目标

使用 FullyShardedDataParallel 分片参数、梯度和优化器状态，分析显存收益与通信成本。

## 实现说明

- `train.py` 复用 DDP 任务的模型和数据，通过配置切换 FSDP wrapping 与 sharding strategy。
- 自动包装策略按模型层边界分片，避免把过小模块切得过碎。
- checkpoint 代码显式选择状态字典类型，并记录加载所需的 world size 与版本信息。

## 学习与复现

1. 选择单卡显存压力明显的模型。
2. 定义合理的自动包装策略。
3. 启动 FSDP 训练并记录各卡显存。
4. 对比不同 sharding strategy。
5. 保存并加载兼容的模型状态。
6. 使用与 DDP 相同的全局 batch 运行 FSDP，并采集峰值显存和 step 时间。
7. 扩展实验：比较两种 wrapping 粒度，观察显存和通信变化。

## 验收标准

- FSDP 训练 loss 正常下降。
- 显存占用低于对应 DDP 实验。
- 能解释分片粒度、通信量和吞吐之间的关系。

## 产出

- FSDP 训练配置与代码。
- DDP/FSDP 显存和性能报告。
