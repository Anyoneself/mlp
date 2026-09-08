# KubeRay RayService

**阶段：** KubeRay  
**建议时间：** 第 15 周前半段  
**前置条件：** 完成任务 27-28

## 目标

使用 RayService 和 Ray Serve 发布具备健康检查与滚动升级能力的 HTTP 服务。

## 实现说明

- `serve_app.py` 定义单一 HTTP Deployment，并暴露版本和健康信息。
- `rayservice.yaml` 同时声明 RayCluster 配置和 Serve application，入口 Service 不暴露管理端口。
- `load_test.py` 在升级前后持续请求，记录错误率、版本切换和延迟。

## 学习与复现

1. 编写最小 Ray Serve Deployment。
2. 创建 RayService，配置服务入口和健康检查。
3. 发送并发请求并记录成功率与延迟。
4. 修改应用版本，观察滚动升级过程。
5. 验证旧版本排空和新版本就绪。
6. 执行 `kubectl apply -f rayservice.yaml`，端口转发服务入口后运行负载脚本。
7. 扩展实验：增加一个副本并修改版本，观察滚动升级期间的响应分布。

## 验收标准

- 服务能够稳定响应并通过健康检查。
- 升级期间没有长时间整体不可用。
- Dashboard 和内部管理端口未暴露公网。

## 产出

- RayService YAML 和 Serve 应用。
- 请求验证与升级记录。
