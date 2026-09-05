# Task Dependency

## 学习目标

将上游任务返回的 `ObjectRef` 直接传给下游任务，构建由 Ray 自动解析的数据依赖。

## 核心 API

- `ObjectRef`：远程对象的引用。
- `function.remote(object_ref)`：把上游结果作为下游任务参数。
- `ray.get()`：只在最终结果处进行同步。

## 执行流程

1. 并行提交两个 `double` 任务。
2. 将两个返回引用直接传给 `add` 任务。
3. Ray 等待上游完成后自动解析参数。
4. 获取并验证最终结果。

## 运行

```bash
python example/19_ray_task_dependency/main.py
```

预期输出：

```text
60
```

## 注意事项

不需要先对上游引用调用 `ray.get()`。直接传递引用可以保留并行性，并让 Ray 调度任务依赖图。
