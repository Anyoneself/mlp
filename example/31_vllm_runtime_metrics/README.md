# vLLM 运行时与指标

**阶段：** vLLM  
**建议时间：** 第 16 周前半段  
**前置条件：** 完成 KubeRay 阶段，具备可用 GPU 环境

## 目标

理解 Prefill、Decode、Continuous Batching、PagedAttention、KV Cache 和关键性能指标。

## 执行步骤

1. 选定可在测试 GPU 上运行的小模型。
2. 启动 vLLM API Server 并发送不同长度请求。
3. 记录 TTFT、TPOT、端到端延迟和 Tokens/s。
4. 观察 Waiting、Running 请求数与 KV Cache 使用率。
5. 改变并发和上下文长度，分析指标变化。

## 验收标准

- 能解释 TTFT 与 TPOT 分别受哪些阶段影响。
- 能说明 KV Cache 为什么限制并发。
- 指标采集脚本能够重复运行。

## 产出

- 启动配置和指标采集脚本。
- 运行时数据流图。
