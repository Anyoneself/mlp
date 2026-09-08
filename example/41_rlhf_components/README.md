# RLHF 角色与数据流

**阶段：** veRL/RLHF  
**建议时间：** 第 22 周前半段  
**前置条件：** 完成 Ray Core、vLLM 和分布式训练阶段

## 目标

理解 Actor、Critic、Reward、Reference Model、Rollout 和更新阶段的职责。

## 实现说明

- `flow.md` 用一条样本贯穿 Prompt、Rollout、Reward、Advantage、Loss 和参数更新。
- `memory_estimator.py` 以模型参数量、dtype、优化器和 KV Cache 配置估算各角色显存。
- `topology.md` 对比模型共置与分离部署，标出参数同步和大张量传输。

## 学习与复现

1. 绘制 Prompt 到 Rollout、Reward、Advantage 和 Update 的数据流。
2. 标注每个模型的输入、输出和是否参与反向传播。
3. 比较 PPO 与 GRPO 对 Critic 和 advantage 的需求。
4. 估算各模型权重、KV Cache 和训练状态显存。
5. 设计模型共置与分离部署方案。
6. 用一个人工构造的两条响应样例手算 reward 和 advantage，再与脚本结果对照。
7. 扩展实验：比较 PPO 与 GRPO 的角色数量和显存估算。

## 验收标准

- 能独立解释各角色及其通信关系。
- 能指出生成和训练阶段的资源峰值。
- 能说明 PPO 与 GRPO 的核心工程差异。

## 产出

- RLHF 数据流和资源拓扑图。
- 关键概念说明。
