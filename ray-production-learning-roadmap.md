# Ray 与 AI 分布式调度生产化学习路线

> 计划基线：2026-09-05  
> 建议周期：24 周  
> 建议投入：每周 10-15 小时  
> 目标方向：Kubernetes 调度、Ray/KubeRay、vLLM、分布式训练、资源效率优化

## 1. 学习目标

完成这条路线后，应具备以下能力：

1. 理解 Kubernetes、Ray 和模型 Runtime 三层调度的职责边界。
2. 能够分析 Pod 为什么被调度到某个 Node、Zone 或 GPU 节点池。
3. 能够开发或扩展 Kubernetes Scheduler Plugin。
4. 能够使用 Ray Core、Ray Serve 和 KubeRay 构建生产服务。
5. 能够部署和优化单机、多卡及多机 vLLM 推理服务。
6. 理解 DDP、FSDP、Tensor Parallel、Pipeline Parallel 等分布式训练技术。
7. 能够设计优先级、抢占、Gang Scheduling、资源混部和自动扩缩容方案。
8. 能够通过压测和监控衡量吞吐、延迟、GPU 利用率及单位请求成本。

## 2. 岗位能力拆分

### 2.1 必须深入掌握

- Linux 进程、网络、文件系统、cgroup 和容器基础
- Go 并发、接口、测试、性能分析
- Python 并发、异步编程和 AI 生态
- Kubernetes Pod、Node、Namespace、Deployment、Service
- Kubernetes Scheduler Framework
- GPU 资源、NVIDIA Device Plugin、MIG、NCCL
- Ray Core、Ray Serve、KubeRay
- vLLM 调度、KV Cache、Continuous Batching、模型并行

### 2.2 需要具备实践能力

- Prometheus、Grafana、日志与链路排查
- Autoscaling、容量规划和负载建模
- PyTorch Distributed、DDP、FSDP
- Placement Group 和 Gang Scheduling
- Priority、Preemption、PDB 和故障恢复
- 多 Zone、多节点池和异构资源调度

### 2.3 需要理解设计思想

- Gödel Scheduler
- YARN、Flink、MapReduce、Mesos、Celery
- veRL、RLHF、GRPO/PPO
- 多集群、多地域和多云调度
- 推荐广告系统的在线训练、推理和 MLOps

不建议平均投入时间。学习深度建议为：

```text
Kubernetes Scheduler > Ray/KubeRay > vLLM
> PyTorch Distributed/veRL
> Gödel/YARN/Flink/Mesos/Celery
```

## 3. 三层调度模型

学习过程中始终使用下面的模型分析系统：

```text
第一层：Kubernetes Scheduler
  将 Pod 调度到具体 Node

第二层：Ray Scheduler
  将 Task、Actor 和 Placement Group 调度到 Ray Worker

第三层：模型 Runtime
  vLLM/PyTorch 决定请求批处理、模型切分和 GPU 通信
```

三者的典型关系：

```text
Kubernetes Cluster
├── Ray Head Pod
├── CPU Ray Worker Pods
└── GPU Ray Worker Pods
    └── vLLM Worker / Training Worker
```

## 4. 24 周学习计划

| 阶段 | 周期 | 核心主题 | 主要产出 |
|---|---:|---|---|
| 阶段 0 | 第 1-2 周 | Linux、Go、Python、容器 | 基础排障手册 |
| 阶段 1 | 第 3-5 周 | Kubernetes 基础调度 | Pod 调度实验集 |
| 阶段 2 | 第 6-8 周 | Scheduler Framework | 自定义 Scheduler Plugin |
| 阶段 3 | 第 9-10 周 | 调度算法与资源模型 | 调度模拟器 |
| 阶段 4 | 第 11-13 周 | Ray Core | Ray 分布式任务项目 |
| 阶段 5 | 第 14-15 周 | KubeRay 与 Ray Serve | RayService 生产部署 |
| 阶段 6 | 第 16-18 周 | vLLM 推理系统 | 三种部署模式压测 |
| 阶段 7 | 第 19-21 周 | 分布式训练 | 多卡训练与恢复实验 |
| 阶段 8 | 第 22 周 | veRL/RLHF | 小模型强化学习实验 |
| 阶段 9 | 第 23-24 周 | 综合生产项目 | 设计、代码、监控、压测报告 |

## 5. 阶段 0：工程基础

### 学习内容

- Linux 进程、线程、信号、文件描述符
- CPU、内存、磁盘和网络观察工具
- Namespace、cgroup 与容器隔离
- Docker 镜像、分层、运行时和网络
- Go goroutine、channel、context、interface、pprof
- Python multiprocessing、asyncio、类型标注和测试

### 实验任务

1. 使用 `top`、`ps`、`lsof`、`ss`、`vmstat` 分析服务状态。
2. 查看容器的 CPU 和内存限制。
3. 编写 Go Worker Pool。
4. 编写 Python 异步任务队列。
5. 对一个服务进行 CPU 和内存 Profiling。

### 验收标准

- 能解释容器限制与 Kubernetes requests/limits 的关系。
- 能定位 CPU 饱和、内存不足、端口占用和进程退出问题。
- 能编写带超时、取消、重试和指标的并发程序。

## 6. 阶段 1：Kubernetes 基础调度

### 学习内容

- Cluster、Node、Zone、Namespace、Pod 的关系
- Pod 生命周期与控制器
- requests、limits 和 QoS
- label、nodeSelector、nodeAffinity
- taint、toleration
- PodAffinity、PodAntiAffinity
- topologySpreadConstraints
- cordon、drain、eviction、PDB
- GPU Device Plugin 和扩展资源

### 实验任务

1. 给 Node 添加节点池和 Zone 标签。
2. 使用 `nodeSelector` 将 Pod 调度到指定节点池。
3. 使用 Node Affinity 调度到指定 Zone。
4. 给节点添加 `NoSchedule` 和 `NoExecute` 污点。
5. 使用 toleration 允许特定 Pod 使用 GPU Node。
6. 使用 `drain` 迁移 Deployment Pod。
7. 制造资源不足，让 Pod 进入 Pending，并通过 Events 分析原因。

### 验收标准

- 能从 Pod YAML、Node 标签和 Events 还原一次调度过程。
- 能解释 Pod label 与 Node label 的区别。
- 能解释 `nodeName` 是调度结果还是硬编码绑定。
- 能设计跨 Zone 高可用的 Pod 分布策略。

## 7. 阶段 2：Kubernetes Scheduler Framework

### 学习内容

- Scheduling Queue
- Scheduling Cycle 与 Binding Cycle
- QueueSort
- PreFilter、Filter、PostFilter
- PreScore、Score、NormalizeScore
- Reserve、Permit、PreBind、Bind、PostBind
- PriorityClass 与 Preemption
- Scheduler Profile
- Scheduler Extender 与 Scheduler Plugin 的区别

### 实验项目：GPU 节点打分插件

使用 Go 编写一个 Scheduler Plugin：

1. Filter 阶段过滤 GPU 不足的节点。
2. Score 阶段综合 GPU 利用率和显存碎片打分。
3. 对高优先级推理服务给予额外权重。
4. 暴露 Prometheus 指标。
5. 编写单元测试和调度集成测试。

### 验收指标

- Pod 能由自定义 Scheduler 正确调度。
- 能输出每个 Node 的过滤原因与最终得分。
- 节点不可用时能正常回退，而不是卡死在 Permit/Bind。
- 插件具备测试、日志和可观测性。

## 8. 阶段 3：调度算法与资源模型

### 学习内容

- First Fit、Best Fit、Bin Packing
- Spread 与负载均衡
- Dominant Resource Fairness
- Gang Scheduling
- Backfilling
- Priority 与 Preemption
- Quota、借用与回收
- CPU/GPU/显存多维资源模型
- GPU 碎片和异构 GPU 调度
- 在线与离线任务混部

### 实验项目：调度模拟器

使用 Python 或 Go 实现离线模拟器，输入：

- Node CPU、内存、GPU 和 Zone
- Job 资源需求、优先级和运行时间
- 不同调度策略

输出：

- 集群利用率
- Job 排队时间
- 抢占次数
- GPU 碎片率
- 调度成功率
- 跨 Zone 调度比例

### 验收标准

- 能用数据说明 Bin Packing 与 Spread 的适用场景。
- 能解释为什么提高利用率可能损害延迟和故障隔离。
- 能设计高低优先级业务的借用、抢占和回收规则。

## 9. 阶段 4：Ray Core

### 学习内容

- `ray.init()`
- Remote Task
- Actor
- ObjectRef 与 Object Store
- Task dependency
- CPU、GPU 与 custom resources
- Placement Group
- PACK、SPREAD、STRICT_PACK、STRICT_SPREAD
- Task retry 与 Actor restart
- Runtime Environment
- Ray Dashboard、State API 和 Timeline

### 实验项目

构建一个 CPU/GPU 混合流水线：

```text
数据读取 Task
  → CPU 预处理 Task
  → GPU Model Actor
  → CPU 后处理 Task
```

要求：

- 为每个任务声明 CPU/GPU。
- 使用多个长期存活的 Model Actor。
- 使用 Placement Group 控制部署位置。
- 模拟 Worker 退出并验证任务恢复。
- 记录每个阶段的排队和执行时间。

### 验收标准

- 能解释 Task、Actor 和 Pod 的区别。
- 能解释 Ray 的逻辑资源不是操作系统级硬隔离。
- 能解释 Ray Scheduler 与 kube-scheduler 的职责边界。
- 能从 Ray Dashboard 定位 Pending Task 原因。

## 10. 阶段 5：KubeRay 与 Ray Serve

### 学习内容

- KubeRay Operator
- RayCluster
- RayJob
- RayService
- Head Group 与 Worker Group
- CPU/GPU Worker Group 隔离
- Ray Autoscaler
- Ray Serve Deployment 与 Replica
- 健康检查、滚动升级和故障恢复

### 实验项目

在 Kubernetes 中部署：

```text
RayService
├── Head Pod
├── CPU Worker Group
└── GPU Worker Group
```

加入：

- `nodeSelector`
- toleration
- Zone Affinity
- requests/limits
- 最小和最大 Worker 数
- Prometheus 指标
- 集中日志

### 验收标准

- 能提交 RayJob 并查看运行状态。
- 能通过 RayService 发布 HTTP 服务。
- 能触发 Worker 自动扩容和缩容。
- 单个 Worker 或 Node 退出后服务能够恢复。
- Dashboard 和内部端口不直接暴露公网。

## 11. 阶段 6：vLLM 推理系统

### 学习内容

- 模型加载与显存组成
- PagedAttention 与 KV Cache
- Continuous Batching
- Prefill 与 Decode
- TTFT、TPOT、E2E Latency、Tokens/s
- `max-model-len`
- `max-num-seqs`
- `gpu-memory-utilization`
- Prefix Caching
- FP8 与其他量化方式
- Tensor Parallel
- Pipeline Parallel
- Data Parallel
- Ray Distributed Executor

### 三组对比实验

#### 实验 A：单 Pod 单 GPU

```text
TP=1, PP=1
```

#### 实验 B：单 Pod 多 GPU

```text
TP=GPU 数量
默认使用本机多进程执行
```

#### 实验 C：KubeRay 多节点

```text
Ray Worker 跨 Node
TP 与 PP 组合
```

### 压测指标

- 请求吞吐
- Output Tokens/s
- P50/P95/P99 TTFT
- P50/P95/P99 TPOT
- GPU 利用率
- GPU 显存和 KV Cache 使用率
- Waiting/Running 请求数
- OOM 次数
- 单位请求或单位 Token 成本

### 验收标准

- 能根据模型大小计算最低 GPU 数量。
- 能区分 API Server 并发、模型副本和模型并行。
- 能解释何时使用 Ray，何时直接部署 vLLM。
- 能通过压测调整并发、上下文长度和显存利用率。

## 12. 阶段 7：分布式训练

### 学习内容

- PyTorch Distributed
- Process Group
- NCCL Collective
- AllReduce、AllGather、ReduceScatter
- DDP
- FSDP
- Tensor Parallel
- Pipeline Parallel
- Data Parallel
- Checkpoint 与恢复
- Elastic Training
- 通信与计算重叠

### 实验任务

1. 单机双卡运行 DDP。
2. 对比单卡和双卡吞吐。
3. 使用 FSDP 训练无法完整放入单卡的模型。
4. 模拟 Worker 退出。
5. 保存并恢复分布式 Checkpoint。
6. 记录 GPU 利用率和 NCCL 通信时间。

### 验收标准

- 能解释 DDP 与 FSDP 的内存差异。
- 能解释 TP、PP、DP 的通信模式。
- 能分析扩卡后吞吐没有线性增长的原因。
- 能处理训练挂起、NCCL 超时和 Checkpoint 恢复问题。

## 13. 阶段 8：veRL 与推荐模型训练

### 学习内容

- RLHF 基本流程
- PPO 与 GRPO
- Actor、Critic、Reward、Reference Model
- Rollout Generation
- veRL WorkerGroup
- Ray 在 RL 训练中的任务编排
- vLLM/SGLang 在 Rollout 中的角色
- 训练与推理之间的参数同步

### 实验任务

- 使用小模型跑通 veRL 官方示例。
- 观察 Ray Actor 和 Placement Group。
- 记录 Rollout、Reward 和 Update 各阶段耗时。
- 分析 GPU 在训练和生成阶段的空闲时间。

### 验收标准

- 能画出 veRL 的分布式执行拓扑。
- 能解释为什么 RL 训练需要复杂的资源编排。
- 能提出减少 GPU 空闲和阶段阻塞的方案。

## 14. 阶段 9：综合生产项目

### 项目目标

构建面向推荐广告场景的 AI 推理与调度平台：

```text
Client
  → Ingress/Gateway
  → Ray Serve Router
  → CPU 图片或特征预处理
  → GPU vLLM/Embedding Actor
  → CPU 后处理
  → Response
```

### 必做功能

- CPU/GPU Worker Group
- GPU Node Pool 与 toleration
- 多 Zone 调度
- Placement Group
- 高低优先级队列
- 抢占或资源回收
- 自动扩缩容
- 节点故障恢复
- Prometheus/Grafana
- 压测和容量模型

### 对比基线

实现两套架构：

1. Kubernetes Deployment 直接部署 vLLM。
2. KubeRay + RayService + vLLM。

对比：

- 部署复杂度
- 请求吞吐
- P95 延迟
- GPU 利用率
- 扩容速度
- 节点故障恢复时间
- 多模型资源共享能力
- 单位 Token 成本

### 最终交付物

- 架构设计文档
- Kubernetes/KubeRay YAML
- Go Scheduler Plugin
- Ray Serve 应用
- vLLM 启动配置
- Prometheus Dashboard
- 压测脚本
- 性能分析报告
- 故障演练报告
- 后续优化列表

## 15. 生产环境检查清单

### 资源和调度

- 是否为所有 Pod 配置 requests/limits
- 是否区分 CPU 与 GPU 节点池
- 是否正确设置 taint/toleration
- 是否存在跨 Zone 通信开销
- Placement Group 是否可能长期 Pending
- 高优先级任务是否会导致低优先级任务饥饿

### 稳定性

- Head、Worker、Actor、Task 的失败策略是否明确
- 是否具有优雅退出和请求排空能力
- 是否配置 PDB 和终止宽限期
- 节点退出后是否能够恢复
- Checkpoint 和模型文件是否依赖本地 `hostPath`

### 可观测性

- API 请求量、错误率、延迟
- Task/Actor Pending 数量
- Worker 数量与扩缩容状态
- GPU 利用率、显存、温度
- vLLM TTFT、TPOT、KV Cache
- 排队时间、执行时间和失败原因

### 安全

- Ray Dashboard 不暴露公网
- API 入口具有鉴权和 TLS
- 使用最小权限 ServiceAccount
- 配置 NetworkPolicy
- 模型远程代码仅加载可信来源

## 16. 每周学习模板

建议每周按以下比例执行：

```text
20%：阅读官方文档和源码
20%：整理概念与架构图
40%：动手实验和编码
20%：压测、复盘和输出文档
```

每周至少产出：

1. 一份概念笔记。
2. 一个可运行实验。
3. 一张架构图或时序图。
4. 一份问题与排查记录。
5. 一次结果复盘。

## 17. 阶段性面试自测

### Kubernetes

- kube-scheduler 如何为 Pod 选择 Node？
- Filter、Score、Reserve、Permit、Bind 分别做什么？
- `nodeSelector`、Affinity、taint/toleration 有什么区别？
- 如何实现 GPU Gang Scheduling？
- 如何减少 GPU 碎片并提升利用率？

### Ray

- Task 和 Actor 有什么区别？
- Ray Scheduler 与 kube-scheduler 如何配合？
- Placement Group 为什么会 Pending？
- Ray Autoscaler 和 Kubernetes Autoscaler 有什么区别？
- Ray Worker 退出后，Actor 和 Task 如何恢复？

### vLLM

- `max-num-seqs` 控制什么？
- 为什么提高并发可能导致 TTFT 变差？
- TP、PP、DP 分别适用于什么场景？
- KV Cache 为什么会限制并发？
- 为什么单模型单卡通常不需要 Ray？

### 系统设计

- 如何设计高低优先级服务的抢占和回收？
- 如何在多个 GPU 节点池之间借用资源？
- 如何处理多 Zone 的容量和故障？
- 如何设计模型服务的容量预测和自动扩缩容？
- 如何证明一个调度策略确实提高了单位算力产出？

## 18. 推荐学习资料

### Kubernetes

- [Kubernetes Scheduling Framework](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/)
- [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
- [Kubernetes Scheduler Plugins](https://github.com/kubernetes-sigs/scheduler-plugins)

### Ray

- [Ray Core](https://docs.ray.io/en/latest/ray-core/walkthrough.html)
- [Ray Scheduling](https://docs.ray.io/en/latest/ray-core/scheduling/index.html)
- [Placement Groups](https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html)
- [KubeRay](https://docs.ray.io/en/latest/cluster/kubernetes/index.html)
- [Ray Serve Production Guide](https://docs.ray.io/en/latest/serve/production-guide/index.html)

### vLLM

- [vLLM Documentation](https://docs.vllm.ai/)
- [Parallelism and Scaling](https://docs.vllm.ai/en/latest/serving/parallelism_scaling/)
- [vLLM Metrics](https://docs.vllm.ai/en/latest/usage/metrics/)

### 分布式训练

- [PyTorch Distributed](https://docs.pytorch.org/docs/stable/distributed.html)
- [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html)
- [NVIDIA NCCL](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/)
- [veRL](https://verl.readthedocs.io/)

### 调度系统

- [Gödel Scheduler](https://github.com/kubewharf/godel-scheduler)
- [Apache YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html)
- [Apache Flink](https://flink.apache.org/)
- [Apache Mesos](https://mesos.apache.org/)
- [Celery](https://docs.celeryq.dev/)

## 19. 执行原则

1. 优先完成 Kubernetes、Ray 和 vLLM 主线。
2. 每个概念必须通过实验验证。
3. 每个实验必须记录指标和失败原因。
4. 不追求一次掌握所有框架，重点学习可迁移的调度思想。
5. 最终评价标准不是“看过多少文档”，而是能否设计、实现、压测和解释一个生产系统。
