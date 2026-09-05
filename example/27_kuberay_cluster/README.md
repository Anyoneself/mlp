# KubeRay RayCluster

**阶段：** KubeRay  
**建议时间：** 第 14 周前半段  
**前置条件：** 完成 Ray Core，准备 Kubernetes 测试集群

## 目标

安装 KubeRay Operator，并部署包含 Head、CPU Worker 和 GPU Worker Group 的 RayCluster。

## 执行步骤

1. 安装并确认 KubeRay Operator 正常运行。
2. 编写 RayCluster 清单，配置 Head 与多个 Worker Group。
3. 为所有容器配置 requests/limits。
4. 为 Worker Group 添加节点选择和容忍规则。
5. 通过端口转发访问 Dashboard，不直接暴露公网。

## 验收标准

- RayCluster 进入 Ready，所有 Pod 调度位置符合预期。
- Head 与 Worker 能互相发现并注册资源。
- 删除一个 Worker 后控制器能够恢复副本。

## 产出

- RayCluster YAML。
- 集群资源拓扑和部署记录。
