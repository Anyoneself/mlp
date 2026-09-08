# KubeRay RayJob

**阶段：** KubeRay  
**建议时间：** 第 14 周后半段  
**前置条件：** 完成任务 27

## 目标

使用 RayJob 提交一次性分布式任务，并管理提交、运行、完成和清理生命周期。

## 实现说明

- `job.py` 是幂等的 Ray 应用入口，输出输入参数、任务结果和退出状态。
- `rayjob.yaml` 固定镜像、入口命令、runtime environment、超时和删除策略。
- `verify.sh` 汇总 RayJob condition、Driver 日志和底层 RayCluster 状态。

## 学习与复现

1. 准备可重复执行的 Ray 作业入口。
2. 编写 RayJob 清单和 runtime environment。
3. 提交作业并观察 Job、RayCluster 和 Pod 状态。
4. 收集 Driver 与 Worker 日志。
5. 测试成功、应用失败和超时场景。
6. 使用 `kubectl apply -f rayjob.yaml` 提交，随后通过 `kubectl describe rayjob` 和日志完成验收。
7. 扩展实验：让作业返回非零退出码，验证 RayJob 状态与清理策略。

## 验收标准

- RayJob 状态与应用退出码一致。
- 失败原因可从状态和日志定位。
- 清理策略不会误删仍需保留的结果。

## 产出

- RayJob YAML 和作业源码。
- 生命周期与失败处理记录。
