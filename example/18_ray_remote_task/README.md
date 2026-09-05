# Remote Task

## 学习目标

使用 `@ray.remote` 将普通 Python 函数声明为 Ray Remote Task，并并行提交多个任务。

## 核心 API

- `@ray.remote`：声明远程函数。
- `function.remote()`：异步提交任务并返回 `ObjectRef`。
- `ray.get()`：等待任务完成并获取结果。

## 执行流程

1. 启动一个具有 2 个逻辑 CPU 的本地 Ray 实例。
2. 并行提交 5 个平方计算任务。
3. 一次性获取全部结果并验证。
4. 关闭 Ray。

## 运行

在项目根目录执行：

```bash
python example/18_ray_remote_task/main.py
```

预期输出：

```text
[0, 1, 4, 9, 16]
```

## 注意事项

`.remote()` 是异步调用；只有执行 `ray.get()` 时，当前进程才会等待对应结果。
