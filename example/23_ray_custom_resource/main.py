"""演示使用自定义逻辑资源约束任务调度。"""

import ray


@ray.remote(resources={"accelerator_type_a": 1})
def use_accelerator() -> str:
    resources = ray.get_runtime_context().get_assigned_resources()
    assert resources["accelerator_type_a"] == 1
    return "scheduled"


def main() -> None:
    ray.init(num_cpus=1, resources={"accelerator_type_a": 1})
    try:
        result = ray.get(use_accelerator.remote())
        assert result == "scheduled"
        print(result)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
