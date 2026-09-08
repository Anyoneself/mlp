# Megatron 与 Embedding 场景

**阶段：** 分布式训练  
**建议时间：** 第 21 周  
**前置条件：** 完成任务 36-39

## 目标

理解 Tensor、Pipeline、Data Parallel 在 Megatron 风格训练中的组合，并应用到 Embedding 模型。

## 实现说明

- `topology.py` 根据 world size、TP、PP、DP 计算每个 Rank 所属通信组并输出拓扑。
- `train.py` 选择可在测试硬件运行的小型双塔或 Embedding 模型，固定数据和负采样。
- `benchmark.py` 分离记录数据加载、Embedding 查找、负样本、前后向和 collective 时间。

## 学习与复现

1. 绘制 TP、PP、DP 的进程拓扑和通信组。
2. 选择小型 Embedding 或双塔模型作为实验对象。
3. 实现或运行最小并行训练配置。
4. 记录计算、通信、数据加载和负样本阶段耗时。
5. 对比至少两种并行组合。
6. 先运行拓扑脚本验证并行维度，再启动最小训练，避免直接调试完整框架。
7. 扩展实验：保持 world size 不变，交换 TP 与 DP 比例并解释性能变化。

## 验收标准

- World Size 与并行维度乘积一致。
- 能解释 Embedding 表、负样本和通信的主要瓶颈。
- 并行方案选择有模型规模和硬件依据。

## 产出

- 并行拓扑图和训练配置。
- 性能瓶颈分析。
