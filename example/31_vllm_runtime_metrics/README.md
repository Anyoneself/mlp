# vLLM 运行时与指标

**阶段：** vLLM  
**建议时间：** 第 16 周前半段  
**前置条件：** 完成 KubeRay 阶段，具备可用 GPU 环境

## 目标

理解 Prefill、Decode、Continuous Batching、PagedAttention、KV Cache 和关键性能指标。

## 实现说明

- `start_server.sh` 固定模型、dtype、上下文长度、并发和显存利用率参数。
- `request.py` 发送可配置输入/输出长度的请求，并记录 TTFT、TPOT 和端到端延迟。
- `collect_metrics.sh` 采集 vLLM 指标与 GPU 指标，所有实验写入带时间戳的结果文件。

## 学习与复现

1. 选定可在测试 GPU 上运行的小模型。
2. 启动 vLLM API Server 并发送不同长度请求。
3. 记录 TTFT、TPOT、端到端延迟和 Tokens/s。
4. 观察 Waiting、Running 请求数与 KV Cache 使用率。
5. 改变并发和上下文长度，分析指标变化。
6. 先用单请求确认指标定义，再逐步增加并发，避免直接从饱和状态开始。
7. 扩展实验：固定并发，只改变输入长度，区分 Prefill 与 Decode 的影响。

## 验收标准

- 能解释 TTFT 与 TPOT 分别受哪些阶段影响。
- 能说明 KV Cache 为什么限制并发。
- 指标采集脚本能够重复运行。

## 产出

- 启动配置和指标采集脚本。
- 运行时数据流图。
