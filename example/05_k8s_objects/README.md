# Kubernetes 核心对象

**阶段：** Kubernetes 基础  
**建议时间：** 第 3 周前半段  
**前置条件：** 完成基础阶段，准备本地测试集群

## 目标

理解 Pod、Node、Namespace、Deployment、Service 的关系和职责边界。

## 实现说明

- 使用 Namespace 隔离实验资源，Deployment 管理无状态应用副本，Service 提供稳定访问入口。
- YAML 拆分为命名空间、工作负载和服务三个文件，便于单独观察每类对象。
- 应用提供健康检查端点，并在 Pod 模板中配置资源和探针。

## 学习与复现

1. 创建独立 Namespace。
2. 部署一个包含 requests/limits 的 Deployment。
3. 创建 ClusterIP Service 并验证访问。
4. 扩缩 Deployment，观察 Pod 与 ReplicaSet 变化。
5. 删除单个 Pod，观察控制器恢复行为。
6. 扩展实验：把副本数改为 3，比较 Pod IP 与 Service 地址是否变化。

## 验收标准

- 能从 Deployment 追踪到 ReplicaSet 和 Pod。
- 能说明 Pod IP 与 Service 虚拟 IP 的区别。
- 能解释删除 Pod 后为何会被重新创建。

## 产出

- Kubernetes YAML。
- 对象关系图和实验记录。
