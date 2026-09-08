# KubeRay 自动扩缩容与恢复

**阶段：** KubeRay  
**建议时间：** 第 15 周后半段  
**前置条件：** 完成任务 29

## 目标

验证 Ray Autoscaler、Worker 故障恢复和节点容量变化时的服务行为。

## 实现说明

- 在 RayCluster 或 RayService 中配置 Worker Group 的最小、最大副本及空闲缩容参数。
- `load_generator.py` 生成可控积压，`observe.sh` 周期采集 Ray 资源、Pod 数量和 Pending 原因。
- 故障脚本只针对明确的测试 Namespace 和带实验标签的 Worker，避免操作其他资源。

## 学习与复现

1. 为 Worker Group 配置最小、最大副本和空闲缩容参数。
2. 提交超过当前容量的负载，观察扩容。
3. 停止负载并观察缩容。
4. 删除 Worker Pod，记录任务和副本恢复。
5. 模拟节点不可用并分析 Kubernetes 与 Ray 两层恢复。
6. 先运行负载触发扩容，再停止负载等待缩容，并保存完整时间线。
7. 扩展实验：在扩容过程中删除一个 Worker，区分替换副本与新增容量。

## 验收标准

- 扩缩容触发原因和耗时可观测。
- Worker 丢失后服务恢复，失败请求边界明确。
- 能区分 Ray Autoscaler 与集群节点 Autoscaler 的职责。

## 产出

- 自动扩缩容配置。
- 扩容、缩容和故障恢复时间线。
