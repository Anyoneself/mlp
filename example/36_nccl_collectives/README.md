# NCCL 集合通信

**阶段：** 分布式训练  
**建议时间：** 第 19 周前半段  
**前置条件：** 完成 vLLM 阶段，具备多 GPU 环境

## 目标

理解 Process Group、Rank、World Size，以及 AllReduce、AllGather 和 ReduceScatter 的数据流。

## 实现说明

- `main.py` 从环境变量读取 rank、local rank 和 world size，初始化 NCCL Process Group 后绑定本地 GPU。
- 每种 collective 使用可手工计算的小张量，并在所有 Rank 上断言结果。
- 计时前执行 warmup 和同步，日志包含 Rank、张量大小、操作类型和耗时。

## 学习与复现

1. 启动双进程 NCCL Process Group。
2. 为每个 Rank 创建可识别的张量。
3. 分别执行 AllReduce、AllGather 和 ReduceScatter。
4. 验证各 Rank 结果。
5. 记录通信数据量、耗时和 NCCL 调试日志。
6. 使用 `torchrun --standalone --nproc-per-node=2 main.py` 运行基线。
7. 扩展实验：改变张量大小，观察启动开销和带宽主导区间。

## 验收标准

- 能画出三种集合通信的数据流。
- 每个 Rank 的结果与手工计算一致。
- 能定位 Rank、端口或网卡配置错误。

## 产出

- 集合通信示例。
- 通信模式与常见故障说明。
