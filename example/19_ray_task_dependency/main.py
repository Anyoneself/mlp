"""演示使用 ObjectRef 建立任务依赖。"""

import ray


@ray.remote
def double(value: int) -> int:
    return value * 2


@ray.remote
def add(left: int, right: int) -> int:
    return left + right


def main() -> None:
    ray.init(num_cpus=2)
    try:
        left_ref = double.remote(10)
        right_ref = double.remote(20)
        total = ray.get(add.remote(left_ref, right_ref))
        assert total == 60
        print(total)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
