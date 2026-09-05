# NCCL 集合通信

**阶段：** 分布式训练  
**建议时间：** 第 19 周前半段  
**前置条件：** 完成 vLLM 阶段，具备多 GPU 环境

## 目标

理解 Process Group、Rank、World Size，以及 AllReduce、AllGather 和 ReduceScatter 的数据流。

## 执行步骤

1. 启动双进程 NCCL Process Group。
2. 为每个 Rank 创建可识别的张量。
3. 分别执行 AllReduce、AllGather 和 ReduceScatter。
4. 验证各 Rank 结果。
5. 记录通信数据量、耗时和 NCCL 调试日志。

## 验收标准

- 能画出三种集合通信的数据流。
- 每个 Rank 的结果与手工计算一致。
- 能定位 Rank、端口或网卡配置错误。

## 产出

- 集合通信示例。
- 通信模式与常见故障说明。
