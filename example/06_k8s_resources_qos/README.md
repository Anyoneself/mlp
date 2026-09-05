# Kubernetes 资源与 QoS

**阶段：** Kubernetes 基础  
**建议时间：** 第 3 周后半段  
**前置条件：** 完成任务 05

## 目标

掌握 requests、limits、QoS、资源不足和 OOM 的基本行为。

## 执行步骤

1. 创建 Guaranteed、Burstable 和 BestEffort 三类 Pod。
2. 查看 Pod QoS 分类和节点可分配资源。
3. 提交 requests 超过节点剩余容量的 Pod。
4. 创建超过内存 limit 的进程并观察退出。
5. 对比 CPU limit 触发限流时的表现。

## 验收标准

- 能根据 YAML 判断 QoS 类别。
- 能区分调度阶段资源不足与运行阶段资源超限。
- 能从 Events 和容器状态定位 Pending 或 OOMKilled。

## 产出

- 三类 QoS 示例 YAML。
- 资源问题对照表。
