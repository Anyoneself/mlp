# Kubernetes 资源与 QoS

**阶段：** Kubernetes 基础  
**建议时间：** 第 3 周后半段  
**前置条件：** 完成任务 05

## 目标

掌握 requests、limits、QoS、资源不足和 OOM 的基本行为。

## 实现说明

- 为 Guaranteed、Burstable、BestEffort 分别准备独立 YAML，保持镜像和命令一致，只改变资源字段。
- 使用一个可配置负载程序分别制造 CPU 压力和内存增长。
- 通过 Pod status、Events、容器退出原因和节点指标建立“配置到现象”的对照。

## 学习与复现

1. 创建 Guaranteed、Burstable 和 BestEffort 三类 Pod。
2. 查看 Pod QoS 分类和节点可分配资源。
3. 提交 requests 超过节点剩余容量的 Pod。
4. 创建超过内存 limit 的进程并观察退出。
5. 对比 CPU limit 触发限流时的表现。
6. 扩展实验：在节点压力下观察三类 Pod 的驱逐顺序。

## 验收标准

- 能根据 YAML 判断 QoS 类别。
- 能区分调度阶段资源不足与运行阶段资源超限。
- 能从 Events 和容器状态定位 Pending 或 OOMKilled。

## 产出

- 三类 QoS 示例 YAML。
- 资源问题对照表。
