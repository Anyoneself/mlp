# Remote Task

## 学习目标

使用 `@ray.remote` 将普通 Python 函数声明为 Ray Remote Task，并并行提交多个任务。

## 核心 API

- `@ray.remote`：声明远程函数。
- `function.remote()`：异步提交任务并返回 `ObjectRef`。
- `ray.get()`：等待任务完成并获取结果。

## 实现说明

- `square()` 保持为无状态纯函数，使用 `@ray.remote` 转换为可调度任务。
- Driver 在列表推导式中先提交全部任务并保存 `ObjectRef`，最后统一 `ray.get()`，避免逐个等待导致串行化。
- `ray.init(num_cpus=2)` 显式限制本地逻辑 CPU，`finally` 保证异常时也能关闭 Ray。

## 学习与复现

1. 先阅读 `main.py`，区分普通函数调用、任务提交和结果同步三个阶段。
2. 安装 Ray 后运行基线命令，确认输出与断言一致。
3. 在 `.remote()` 后打印返回值类型，确认得到的是引用而不是平方结果。
4. 给 `square()` 临时加入短暂休眠，对比统一 `ray.get()` 与循环中逐个 `ray.get()`。
5. 将 `num_cpus` 改为 1 和 4，记录总耗时变化并解释逻辑资源的作用。

## 运行

在项目根目录执行：

```bash
python example/18_ray_remote_task/main.py
```

预期输出：

```text
[0, 1, 4, 9, 16]
```

## 验收标准

- 代码一次提交全部任务，不在提交循环中调用 `ray.get()`。
- 输出与断言一致，异常退出时仍执行 `ray.shutdown()`。
- 能解释 `.remote()`、`ObjectRef` 和 `ray.get()` 各自发生在什么阶段。

## 产出

- 可独立运行的 `main.py`。
- 不同逻辑 CPU 数量下的耗时记录和结论。

## 注意事项

`.remote()` 是异步调用；只有执行 `ray.get()` 时，当前进程才会等待对应结果。
