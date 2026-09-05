"""演示提交并行 Ray Remote Task。"""

import ray


@ray.remote
def square(value: int) -> int:
    return value * value


def main() -> None:
    ray.init(num_cpus=2)
    try:
        results = ray.get([square.remote(value) for value in range(5)])
        assert results == [0, 1, 4, 9, 16]
        print(results)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
