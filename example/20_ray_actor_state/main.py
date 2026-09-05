"""演示使用 Ray Actor 保存可变状态。"""

import ray


@ray.remote
class Counter:
    def __init__(self) -> None:
        self.value = 0

    def increment(self) -> int:
        self.value += 1
        return self.value

    def get(self) -> int:
        return self.value


def main() -> None:
    ray.init()
    try:
        counter = Counter.remote()
        ray.get([counter.increment.remote() for _ in range(3)])
        value = ray.get(counter.get.remote())
        assert value == 3
        print(value)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
