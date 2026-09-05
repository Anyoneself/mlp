# Object Store

## 学习目标

使用 `ray.put()` 将对象写入 Ray Object Store，并通过引用供远程任务读取。

## 核心 API

- `ray.put()`：写入对象并返回 `ObjectRef`。
- `ray.get()`：读取远程对象或任务结果。
- `ObjectRef` 参数：让 Ray 在执行任务前解析对象。

## 执行流程

1. 将只读字典写入 Object Store。
2. 把字典引用和查询键传给远程任务。
3. 任务读取字典并返回查询结果。
4. 验证结果。

## 运行

```bash
python example/21_ray_object_store/main.py
```

预期输出：

```text
distributed
```

## 注意事项

适合复用的较大只读对象可以只执行一次 `ray.put()`。不要在循环中重复写入相同对象。
