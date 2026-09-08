# Kubernetes 污点、Zone 与 GPU

**阶段：** Kubernetes 基础  
**建议时间：** 第 4 周后半段  
**前置条件：** 完成任务 07

## 目标

组合 taint、toleration、Zone Affinity 和扩展资源，隔离 GPU 节点池。

## 实现说明

- 节点侧同时使用专用 label、taint 和 GPU 扩展资源描述能力与准入边界。
- Pod 侧同时声明 toleration、Node Affinity 和资源请求，三者分别解决“允许进入、选择位置、占用容量”。
- 无 GPU 环境用自定义扩展资源模拟调度，不伪造真实 GPU 执行结果。

## 学习与复现

1. 为 GPU 测试节点添加专用 label 和 `NoSchedule` taint。
2. 验证普通 Pod 无法进入该节点。
3. 为 GPU Pod 添加 toleration 与 Node Affinity。
4. 声明 GPU 扩展资源请求；无 GPU 时使用自定义扩展资源模拟。
5. 增加 Zone 约束并记录可调度节点。
6. 扩展实验：分别移除 toleration、Affinity 和资源请求，记录三种不同结果。

## 验收标准

- 普通业务不会误用 GPU 节点。
- GPU Pod 同时满足容忍、节点标签和资源容量要求。
- 能解释 toleration 允许调度但不保证调度。

## 产出

- GPU 节点池隔离 YAML。
- 调度约束分析表。
