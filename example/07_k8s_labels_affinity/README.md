# Kubernetes 标签与亲和性

**阶段：** Kubernetes 基础  
**建议时间：** 第 4 周前半段  
**前置条件：** 完成任务 06

## 目标

使用 label、nodeSelector、Node Affinity 和 Pod Anti-Affinity 控制工作负载位置。

## 实现说明

- 先建立固定的节点标签矩阵，再为每种调度策略准备独立 Pod 或 Deployment YAML。
- 每份 YAML 只改变一种约束，便于确认 nodeSelector、硬亲和性、软亲和性和反亲和性的差异。
- 使用 Pod 到 Node 的映射表记录期望位置与实际位置。

## 学习与复现

1. 给测试节点添加节点池和 Zone 标签。
2. 使用 `nodeSelector` 将 Pod 放入指定节点池。
3. 改用 required Node Affinity 表达相同约束。
4. 使用 preferred Affinity 设置软偏好。
5. 使用 Pod Anti-Affinity 分散多个副本。
6. 扩展实验：移除一个节点标签，预测硬约束和软偏好分别如何表现。

## 验收标准

- 能区分硬约束与软偏好。
- 能从 Pod spec 预测候选节点集合。
- 多副本能够按预期分散，约束无法满足时现象明确。

## 产出

- 四组调度 YAML。
- 每组 Pod 到 Node 的实际映射记录。
