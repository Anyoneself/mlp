# MLP

面向 Kubernetes、Ray、KubeRay、vLLM 和分布式训练的调度与生产化学习项目。

学习主线见 [ray-production-learning-roadmap.md](ray-production-learning-roadmap.md)，AI 编码代理的项目约束见 [AGENTS.md](AGENTS.md)。

## 环境准备

建议使用 Python 3.10、3.11 或 3.12 创建独立环境：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip ray
```

## 任务路线

24 周计划已拆分为 48 个可依次执行的任务。完整顺序、阶段映射和完成状态见 [example/README.md](example/README.md)。

已实现任务可以直接运行，例如：

```bash
python example/18_ray_remote_task/main.py
```

运行所有已经提供 `main.py` 的 Python 示例：

```bash
for file in example/*/main.py; do python "$file"; done
```
