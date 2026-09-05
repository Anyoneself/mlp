# 优先级、抢占与 PDB

**阶段：** Kubernetes 调度器  
**建议时间：** 第 7 周后半段  
**前置条件：** 完成任务 12

## 目标

验证 PriorityClass、Preemption 与 PodDisruptionBudget 的协同行为和限制。

## 执行步骤

1. 创建高、低两级 PriorityClass。
2. 用低优先级 Pod 填满测试节点。
3. 提交高优先级 Pod 并观察抢占候选。
4. 为低优先级服务添加 PDB 后重复实验。
5. 记录被提名节点、驱逐过程和调度延迟。

## 验收标准

- 能解释优先级、抢占资格和 `nominatedNodeName`。
- 能区分自愿中断、调度抢占和 PDB 的适用边界。
- 能说明高优先级任务仍可能 Pending 的原因。

## 产出

- 优先级与 PDB YAML。
- 抢占实验报告。
