# Custom Resource

## 学习目标

声明 Ray 自定义逻辑资源，并让任务只在具备该资源的节点上运行。

## 核心 API

- `ray.init(resources=...)`：为本地节点声明自定义资源。
- `@ray.remote(resources=...)`：声明任务所需资源。
- `get_assigned_resources()`：查看任务实际获得的逻辑资源。

## 执行流程

1. 启动拥有一个 `accelerator_type_a` 资源的本地节点。
2. 提交需要该资源的任务。
3. 在任务中检查已分配资源。
4. 验证任务成功完成。

## 运行

```bash
python example/23_ray_custom_resource/main.py
```

预期输出：

```text
scheduled
```

## 注意事项

自定义资源是 Ray 调度使用的逻辑容量，不代表操作系统级隔离，也不会自动限制真实硬件使用。
