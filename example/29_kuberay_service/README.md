# KubeRay RayService

**阶段：** KubeRay  
**建议时间：** 第 15 周前半段  
**前置条件：** 完成任务 27-28

## 目标

使用 RayService 和 Ray Serve 发布具备健康检查与滚动升级能力的 HTTP 服务。

## 执行步骤

1. 编写最小 Ray Serve Deployment。
2. 创建 RayService，配置服务入口和健康检查。
3. 发送并发请求并记录成功率与延迟。
4. 修改应用版本，观察滚动升级过程。
5. 验证旧版本排空和新版本就绪。

## 验收标准

- 服务能够稳定响应并通过健康检查。
- 升级期间没有长时间整体不可用。
- Dashboard 和内部管理端口未暴露公网。

## 产出

- RayService YAML 和 Serve 应用。
- 请求验证与升级记录。
