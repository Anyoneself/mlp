# PyTorch DDP

**阶段：** 分布式训练  
**建议时间：** 第 19 周后半段  
**前置条件：** 完成任务 36

## 目标

完成单机多卡 DistributedDataParallel 训练并与单卡基线比较。

## 实现说明

- `train.py` 同时支持单进程和 DDP，模型、数据、优化器和随机种子保持一致。
- DDP 模式每个进程绑定一个 GPU，使用 DistributedSampler，并只由 Rank 0 写日志和 checkpoint。
- `benchmark.py` 统一计算样本吞吐、step 时间、显存和扩展效率。

## 学习与复现

1. 创建单卡训练基线。
2. 使用 `torchrun` 启动多进程训练。
3. 使用 DistributedSampler 切分数据。
4. 校验梯度同步、loss 和 checkpoint。
5. 对比吞吐、显存与扩展效率。
6. 先运行 `python train.py` 建立单卡结果，再用 `torchrun --standalone --nproc-per-node=2 train.py` 运行双卡。
7. 扩展实验：改变 batch size，区分全局 batch 变化与纯扩卡效果。

## 验收标准

- 每个 GPU 对应一个训练进程。
- 数据不会在 Rank 间无意重复。
- 多卡模型结果正确，性能差异有解释。

## 产出

- 单卡和 DDP 训练代码。
- 性能对比报告。
