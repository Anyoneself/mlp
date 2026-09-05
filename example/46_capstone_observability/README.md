# 综合项目可观测性

**阶段：** 综合项目  
**建议时间：** 第 23 周后半段  
**前置条件：** 完成任务 44-45

## 目标

建立覆盖 API、Kubernetes、Ray、vLLM 和 GPU 的指标、日志与告警体系。

## 执行步骤

1. 定义请求量、错误率和延迟 SLI。
2. 采集 Pod、Node、Ray Task/Actor 和 Autoscaler 指标。
3. 采集 TTFT、TPOT、KV Cache、GPU 利用率和显存。
4. 建立统一请求 ID 和结构化日志。
5. 创建 Dashboard 与容量、错误、延迟告警。

## 验收标准

- 能从一次慢请求追踪到对应服务和资源状态。
- 告警包含影响、证据和可执行处理建议。
- Dashboard 能支持容量判断和故障定位。

## 产出

- Prometheus 规则和 Grafana Dashboard。
- 日志字段规范与告警手册。
