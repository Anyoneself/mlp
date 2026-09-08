# Object Store

## 学习目标

使用 `ray.put()` 将对象写入 Ray Object Store，并通过引用供远程任务读取。

## 核心 API

- `ray.put()`：写入对象并返回 `ObjectRef`。
- `ray.get()`：读取远程对象或任务结果。
- `ObjectRef` 参数：让 Ray 在执行任务前解析对象。

## 实现说明

- Driver 使用一次 `ray.put()` 将共享字典写入 Object Store。
- 多个任务可复用同一个 `ObjectRef`，任务函数接收到的是 Ray 解析后的字典。
- 示例把共享对象视为只读输入，不依赖任务对它进行原地修改。

## 学习与复现

1. 运行基线并确认任务能够读取共享字典。
2. 打印 `database_ref`，区分引用与对象值。
3. 并行提交多个不同 key 的查询，复用同一个引用。
4. 对比循环内重复 `ray.put()` 与只放置一次的写法。
5. 扩展为较大数组并观察 Object Store 内存，但不要提交大型生成物。

## 运行

```bash
python example/21_ray_object_store/main.py
```

预期输出：

```text
distributed
```

## 验收标准

- 共享对象只执行一次 `ray.put()`，多个任务可以复用同一引用。
- 任务结果正确，Driver 能区分对象值与 `ObjectRef`。
- 能解释为什么共享输入应视为只读数据。

## 产出

- 可独立运行的 `main.py`。
- 单次放置与重复放置的实现和观测对比。

## 注意事项

适合复用的较大只读对象可以只执行一次 `ray.put()`。不要在循环中重复写入相同对象。
