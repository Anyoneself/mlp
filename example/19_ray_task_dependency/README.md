# Task Dependency

## 学习目标

将上游任务返回的 `ObjectRef` 直接传给下游任务，构建由 Ray 自动解析的数据依赖。

## 核心 API

- `ObjectRef`：远程对象的引用。
- `function.remote(object_ref)`：把上游结果作为下游任务参数。
- `ray.get()`：只在最终结果处进行同步。

## 实现说明

- 两个 `double` 任务并行生成上游 `ObjectRef`，Driver 不读取中间结果。
- `add.remote(left_ref, right_ref)` 直接接收引用，Ray 在下游执行前解析依赖。
- Driver 只对最终引用调用一次 `ray.get()`，形成最小任务依赖图。

## 学习与复现

1. 画出两个 `double` 指向一个 `add` 的 DAG，并标出哪些值位于 Driver。
2. 运行基线并确认最终结果为 60。
3. 给两个上游任务设置不同休眠时间，观察下游必须等待两个依赖。
4. 对比“直接传 ObjectRef”和“先 ray.get 再传普通值”两种写法。
5. 增加第三个上游任务，扩展 DAG 并保持 Driver 只同步最终结果。

## 运行

```bash
python example/19_ray_task_dependency/main.py
```

预期输出：

```text
60
```

## 验收标准

- 上游两个任务可以并行，下游任务等待全部依赖后执行。
- Driver 只同步最终结果，没有提前读取上游对象。
- 能画出并解释本示例的任务依赖图。

## 产出

- 可独立运行的 `main.py`。
- 直接传引用与提前 `ray.get()` 的行为对比记录。

## 注意事项

不需要先对上游引用调用 `ray.get()`。直接传递引用可以保留并行性，并让 Ray 调度任务依赖图。
