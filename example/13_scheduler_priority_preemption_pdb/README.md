# 优先级、抢占与 PDB

**阶段：** Kubernetes 调度器  
**建议时间：** 第 7 周后半段  
**前置条件：** 完成任务 12

## 目标

验证 PriorityClass、Preemption 与 PodDisruptionBudget 的协同行为和限制。

## 实现说明

- 用固定资源请求构造节点满载环境，高低优先级工作负载分别放在独立 YAML。
- 采集 Pod Events、`nominatedNodeName`、被抢占 Pod 终止时间和高优先级 Pod 就绪时间。
- PDB 场景与无 PDB 场景保持其他条件一致，避免把控制器副本差异误判为 PDB 效果。

## 学习与复现

1. 创建高、低两级 PriorityClass。
2. 用低优先级 Pod 填满测试节点。
3. 提交高优先级 Pod 并观察抢占候选。
4. 为低优先级服务添加 PDB 后重复实验。
5. 记录被提名节点、驱逐过程和调度延迟。
6. 扩展实验：设置 `preemptionPolicy: Never`，比较高优先级 Pod 的行为。

## 验收标准

- 能解释优先级、抢占资格和 `nominatedNodeName`。
- 能区分自愿中断、调度抢占和 PDB 的适用边界。
- 能说明高优先级任务仍可能 Pending 的原因。

## 产出

- 优先级与 PDB YAML。
- 抢占实验报告。
