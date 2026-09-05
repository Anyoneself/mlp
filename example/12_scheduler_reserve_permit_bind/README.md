# Scheduler Reserve、Permit 与 Bind

**阶段：** Kubernetes 调度器  
**建议时间：** 第 7 周前半段  
**前置条件：** 完成任务 11

## 目标

理解调度后半段的资源预留、等待、回滚和绑定行为。

## 执行步骤

1. 绘制 Reserve、Permit、PreBind、Bind、PostBind 时序。
2. 实现一个内存态 Reserve/Unreserve 示例。
3. 设计 Permit 成功、等待、拒绝和超时场景。
4. 注入绑定失败，验证 Unreserve 被调用。
5. 记录并发调度下共享状态的同步策略。

## 验收标准

- 能解释 Reserve 与真实资源分配的区别。
- 失败路径能够回滚，不遗留占用记录。
- Permit 不会导致无界等待。

## 产出

- 生命周期实验代码。
- 回滚与超时测试记录。
