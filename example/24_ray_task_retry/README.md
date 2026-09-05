# Task Retry

## 学习目标

配置 Ray Task 在遇到指定临时异常时自动重试。

## 核心 API

- `max_retries`：任务失败后的最大重试次数。
- `retry_exceptions`：允许触发重试的应用异常类型。
- Actor：记录跨任务重试保留的尝试次数。

## 执行流程

1. 创建记录调用次数的 `AttemptTracker` Actor。
2. 首次执行任务时主动抛出 `TransientError`。
3. Ray 自动重试任务。
4. 第二次执行成功并返回尝试次数。

## 运行

```bash
python example/24_ray_task_retry/main.py
```

预期输出：

```text
succeeded on attempt 2
```

## 注意事项

重试可能重复执行已经产生的副作用。生产任务应保持幂等，或使用唯一请求 ID、事务等机制防止重复写入。
