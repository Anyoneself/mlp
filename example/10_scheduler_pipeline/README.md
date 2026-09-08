# Kubernetes 调度流程

**阶段：** Kubernetes 调度器  
**建议时间：** 第 6 周前半段  
**前置条件：** 完成 Kubernetes 基础阶段

## 目标

理解 Scheduling Queue、Scheduling Cycle、Binding Cycle 和主要扩展点的调用顺序。

## 实现说明

- 用时序图表示 Pod 从 Active Queue 到 Node 绑定的主路径，并单独标出失败重入队。
- 准备一个最小 Scheduler Profile 和高日志级别配置，用真实日志验证扩展点顺序。
- 将扩展点整理成表格，字段包含输入、输出、是否并发、是否可修改状态和失败后行为。

## 学习与复现

1. 阅读 Scheduler Framework 官方架构说明。
2. 绘制 Pod 从入队到绑定 Node 的时序图。
3. 标注 QueueSort、PreFilter、Filter、Score 和 Bind 的输入输出。
4. 区分 Scheduling Cycle 与 Binding Cycle。
5. 从调度器日志追踪一次实际调度。
6. 扩展实验：制造一次 Filter 全失败，追踪 Pod 如何进入不可调度队列。

## 验收标准

- 能按顺序讲清主要扩展点。
- 能说明哪些阶段只读、哪些阶段可能修改共享状态。
- 能把一条调度日志映射到时序图。

## 产出

- 调度流程图。
- 扩展点职责表。
