# 24 周任务路线

本目录将学习计划拆分为 48 个原子任务。任务采用全局编号，原则上应按顺序执行；每个任务目录中的 `README.md` 给出目标、前置条件、执行步骤、验收标准和产出。

状态说明：

- `[ ]`：尚未完成验收。
- `[x]`：代码或文档已经完成，并通过任务 README 中的验收。

即使目录中已有示例代码，在实际执行并记录结果前也保持未完成状态。

## 统一学习与复现方法

每个任务都按下面的顺序执行：

1. 阅读任务 README 的目标和实现说明，先画出输入、处理过程和输出。
2. 准备 README 指定的本地环境，不直接在生产集群做实验。
3. 阅读已有源码或配置；任务尚未实现时，按文件职责逐个创建。
4. 复制 README 中的命令运行基线实验，保留关键日志、Events 和指标。
5. 对照验收标准判断结果，不以“命令没有报错”代替验收。
6. 修改一个关键参数或注入一个失败场景，解释结果为什么变化。
7. 将命令、环境、结果和结论写入任务目录，验收通过后再勾选状态。

为了让别人能够复现，记录中至少应包含操作系统、语言或框架版本、硬件或集群规格、完整命令、关键配置和实际输出。涉及真实 GPU 或多节点集群的任务，应同时提供低资源替代方案或说明无法替代的原因。

## 第 1-2 周：基础补齐

- [x] `01_linux_process_network`：Linux 进程与网络排障
- [ ] `02_container_cgroup`：容器与 cgroup 资源限制
- [ ] `03_go_concurrency`：Go Worker Pool 与取消
- [ ] `04_python_async`：Python 异步任务队列

## 第 3-5 周：Kubernetes 基础

- [ ] `05_k8s_objects`：Pod、Node、Namespace 与控制器
- [ ] `06_k8s_resources_qos`：requests、limits 与 QoS
- [ ] `07_k8s_labels_affinity`：标签、选择器与亲和性
- [ ] `08_k8s_taints_zones_gpu`：污点、Zone 与 GPU 节点
- [ ] `09_k8s_pending_diagnostics`：Pending Pod 调度排障

## 第 6-8 周：Kubernetes 调度器

- [ ] `10_scheduler_pipeline`：调度周期与扩展点
- [ ] `11_scheduler_filter_score`：Filter 与 Score
- [ ] `12_scheduler_reserve_permit_bind`：Reserve、Permit 与 Bind
- [ ] `13_scheduler_priority_preemption_pdb`：优先级、抢占与 PDB
- [ ] `14_scheduler_plugin`：Go Scheduler Plugin

## 第 9-10 周：调度算法

- [ ] `15_scheduling_binpacking_spread`：Bin Packing 与 Spread
- [ ] `16_scheduling_drf_fairness`：DRF 与公平性
- [ ] `17_scheduling_gang_fragmentation`：Gang Scheduling 与资源碎片

## 第 11-13 周：Ray Core

- [ ] `18_ray_remote_task`：Remote Task
- [ ] `19_ray_task_dependency`：任务依赖
- [ ] `20_ray_actor_state`：Actor 状态
- [ ] `21_ray_object_store`：Object Store
- [ ] `22_ray_wait`：增量等待任务
- [ ] `23_ray_custom_resource`：自定义资源
- [ ] `24_ray_task_retry`：任务重试
- [ ] `25_ray_placement_group`：Placement Group
- [ ] `26_ray_mixed_pipeline`：CPU/GPU 混合流水线

## 第 14-15 周：KubeRay

- [ ] `27_kuberay_cluster`：RayCluster
- [ ] `28_kuberay_job`：RayJob
- [ ] `29_kuberay_service`：RayService
- [ ] `30_kuberay_autoscaling_recovery`：自动扩缩容与故障恢复

## 第 16-18 周：vLLM

- [ ] `31_vllm_runtime_metrics`：推理运行时与指标
- [ ] `32_vllm_single_gpu`：单卡部署
- [ ] `33_vllm_multi_gpu`：单机多卡部署
- [ ] `34_vllm_ray_multinode`：Ray 多节点部署
- [ ] `35_vllm_benchmark`：吞吐与延迟压测

## 第 19-21 周：分布式训练

- [ ] `36_nccl_collectives`：NCCL 集合通信
- [ ] `37_pytorch_ddp`：DDP 训练
- [ ] `38_pytorch_fsdp`：FSDP 训练
- [ ] `39_training_checkpoint_recovery`：Checkpoint 与故障恢复
- [ ] `40_megatron_embedding`：Megatron 与 Embedding 场景

## 第 22 周：veRL/RLHF

- [ ] `41_rlhf_components`：RLHF 角色与数据流
- [ ] `42_verl_worker_group`：Ray WorkerGroup 与 Rollout
- [ ] `43_grpo_ppo`：小模型 GRPO/PPO

## 第 23-24 周：综合项目

- [ ] `44_capstone_architecture`：架构与容量规划
- [ ] `45_capstone_autoscaling_preemption`：扩缩容、抢占与混部
- [ ] `46_capstone_observability`：监控与可观测性
- [ ] `47_capstone_failure_benchmark`：故障演练与压测
- [ ] `48_capstone_final_report`：最终交付与复盘
