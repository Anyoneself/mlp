# Pending Pod 调度排障

**阶段：** Kubernetes 基础  
**建议时间：** 第 5 周  
**前置条件：** 完成任务 05-08

## 目标

建立从 Pod、Events、Node 到调度约束的系统化 Pending 排查流程。

## 执行步骤

1. 分别制造 CPU 不足、标签不匹配、污点不容忍和 PVC 未绑定。
2. 使用 `kubectl describe pod` 收集调度失败事件。
3. 检查 Node label、taint、容量和可分配资源。
4. 为每个故障只修改一个条件并验证恢复。
5. 整理统一排障决策树。

## 验收标准

- 能在 10 分钟内定位四类 Pending 原因。
- 修复依据来自调度事件和配置，而不是反复试错。
- 能区分 Scheduler 问题与镜像拉取、容器启动问题。

## 产出

- `pending-runbook.md`。
- 四组故障复现 YAML。
