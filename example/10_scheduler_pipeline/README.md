# Kubernetes 调度流程

**阶段：** Kubernetes 调度器  
**建议时间：** 第 6 周前半段  
**前置条件：** 完成 Kubernetes 基础阶段

## 目标

理解 Scheduling Queue、Scheduling Cycle、Binding Cycle 和主要扩展点的调用顺序。

## 执行步骤

1. 阅读 Scheduler Framework 官方架构说明。
2. 绘制 Pod 从入队到绑定 Node 的时序图。
3. 标注 QueueSort、PreFilter、Filter、Score 和 Bind 的输入输出。
4. 区分 Scheduling Cycle 与 Binding Cycle。
5. 从调度器日志追踪一次实际调度。

## 验收标准

- 能按顺序讲清主要扩展点。
- 能说明哪些阶段只读、哪些阶段可能修改共享状态。
- 能把一条调度日志映射到时序图。

## 产出

- 调度流程图。
- 扩展点职责表。
