# Actor State

## 学习目标

使用 Ray Actor 创建长期存活的有状态 Worker，并通过方法调用修改和读取状态。

## 核心 API

- `@ray.remote`：将类声明为 Actor。
- `ActorClass.remote()`：创建 Actor 实例。
- `actor.method.remote()`：异步调用 Actor 方法。

## 执行流程

1. 创建一个初始值为 0 的 `Counter` Actor。
2. 提交 3 次递增调用。
3. 读取 Actor 当前状态。
4. 验证最终值为 3。

## 运行

```bash
python example/20_ray_actor_state/main.py
```

预期输出：

```text
3
```

## 注意事项

同一个 Actor 的普通方法默认按顺序执行。Actor 进程退出时，未持久化的内存状态可能丢失。
