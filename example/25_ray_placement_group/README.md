# Placement Group

## 学习目标

使用 Placement Group 原子预留一组资源，并将任务绑定到指定 bundle。

## 核心 API

- `placement_group()`：创建包含多个资源 bundle 的资源组。
- `group.ready()`：等待整个资源组可用。
- `PlacementGroupSchedulingStrategy`：将任务调度到资源组及指定 bundle。
- `remove_placement_group()`：释放预留资源。

## 执行流程

1. 启动具有 2 个逻辑 CPU 的本地 Ray 实例。
2. 创建包含两个 1 CPU bundle 的 Placement Group。
3. 等待资源组完整就绪。
4. 分别向两个 bundle 提交任务。
5. 验证结果并释放资源组。

## 运行

```bash
python example/25_ray_placement_group/main.py
```

预期输出：

```text
placement group tasks completed
```

## 注意事项

Placement Group 需要所有 bundle 能够同时满足才会就绪。资源不足时可能长期 Pending，生产环境应设置超时并观察调度状态。
