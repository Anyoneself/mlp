# Placement Group

## 学习目标

使用 Placement Group 原子预留一组资源，并将任务绑定到指定 bundle。

## 核心 API

- `placement_group()`：创建包含多个资源 bundle 的资源组。
- `group.ready()`：等待整个资源组可用。
- `PlacementGroupSchedulingStrategy`：将任务调度到资源组及指定 bundle。
- `remove_placement_group()`：释放预留资源。

## 实现说明

- Placement Group 由两个 1 CPU bundle 组成，创建时按组原子预留资源。
- 每个任务通过 `PlacementGroupSchedulingStrategy` 绑定到指定 bundle。
- Driver 等待 `group.ready()` 后才提交任务，并在 `finally` 中释放资源组。

## 学习与复现

1. 运行基线并确认两个任务都使用预留资源完成。
2. 将本地 CPU 减为 1，观察资源组无法完整就绪和超时行为。
3. 对比 PACK、SPREAD、STRICT_PACK、STRICT_SPREAD 的调度意图。
4. 去掉任务的 PlacementGroupSchedulingStrategy，理解预留资源不会被普通任务自动使用。
5. 使用状态命令查看资源组状态，并验证释放后资源恢复。

## 运行

```bash
python example/25_ray_placement_group/main.py
```

预期输出：

```text
placement group tasks completed
```

## 验收标准

- Placement Group 完整就绪后任务才开始执行。
- 两个任务分别绑定到指定 bundle，并在结束后释放资源组。
- 资源不足时能观察到 Pending 或超时，而不是无限等待。

## 产出

- 可独立运行的 `main.py`。
- 不同策略、资源不足和资源释放实验记录。

## 注意事项

Placement Group 需要所有 bundle 能够同时满足才会就绪。资源不足时可能长期 Pending，生产环境应设置超时并观察调度状态。
