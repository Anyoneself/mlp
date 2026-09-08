# Actor State

## 学习目标

使用 Ray Actor 创建长期存活的有状态 Worker，并通过方法调用修改和读取状态。

## 核心 API

- `@ray.remote`：将类声明为 Actor。
- `ActorClass.remote()`：创建 Actor 实例。
- `actor.method.remote()`：异步调用 Actor 方法。

## 实现说明

- `Counter` 将状态保存在专用 Actor 进程内，Driver 只持有 Actor Handle。
- 多次 `increment.remote()` 异步提交到同一个 Actor，普通 Actor 按接收顺序处理方法。
- 最后调用 `get()` 读取状态，并用断言验证所有递增已经生效。

## 学习与复现

1. 对比 Task 和 Actor：前者无状态复用 Worker，后者使用专用有状态 Worker。
2. 运行基线并确认最终状态为 3。
3. 创建两个 Counter，验证它们的状态相互独立。
4. 在方法中打印进程 PID，确认同一 Actor 的调用落在同一进程。
5. 主动终止 Actor，观察未配置重启时的错误，并理解内存状态为何丢失。

## 运行

```bash
python example/20_ray_actor_state/main.py
```

预期输出：

```text
3
```

## 验收标准

- 三次递增后 Actor 状态稳定为 3。
- 两个 Actor 实例的状态相互隔离。
- 能说明 Actor 状态位置及进程退出后的状态风险。

## 产出

- 可独立运行的 `main.py`。
- Actor PID、调用顺序和故障行为记录。

## 注意事项

同一个 Actor 的普通方法默认按顺序执行。Actor 进程退出时，未持久化的内存状态可能丢失。
