# Kubernetes 污点、Zone 与 GPU

**阶段：** Kubernetes 基础  
**建议时间：** 第 4 周后半段  
**前置条件：** 完成任务 07

## 目标

组合 taint、toleration、Zone Affinity 和扩展资源，隔离 GPU 节点池。

## 执行步骤

1. 为 GPU 测试节点添加专用 label 和 `NoSchedule` taint。
2. 验证普通 Pod 无法进入该节点。
3. 为 GPU Pod 添加 toleration 与 Node Affinity。
4. 声明 GPU 扩展资源请求；无 GPU 时使用自定义扩展资源模拟。
5. 增加 Zone 约束并记录可调度节点。

## 验收标准

- 普通业务不会误用 GPU 节点。
- GPU Pod 同时满足容忍、节点标签和资源容量要求。
- 能解释 toleration 允许调度但不保证调度。

## 产出

- GPU 节点池隔离 YAML。
- 调度约束分析表。
