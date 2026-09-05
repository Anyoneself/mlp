# veRL WorkerGroup 与 Rollout

**阶段：** veRL/RLHF  
**建议时间：** 第 22 周中段  
**前置条件：** 完成任务 41

## 目标

观察 veRL 如何使用 Ray WorkerGroup 编排 Rollout、Reward 和训练 Worker。

## 执行步骤

1. 选择资源可承受的 veRL 最小官方示例。
2. 记录 Ray Actor、Placement Group 和 GPU 映射。
3. 跟踪一次 Rollout 到参数更新的时序。
4. 采集各阶段执行时间和 GPU 空闲时间。
5. 分析参数同步和阶段屏障。

## 验收标准

- 能从 Ray 状态还原 WorkerGroup 拓扑。
- 能定位至少一个 GPU 空闲或阶段阻塞点。
- 实验配置、模型和数据版本可复现。

## 产出

- WorkerGroup 拓扑图。
- Rollout 时序和资源利用率报告。
