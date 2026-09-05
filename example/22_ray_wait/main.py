"""演示使用 ray.wait() 增量处理已完成的任务。"""

import time

import ray


@ray.remote
def delayed_value(value: int, delay_seconds: float) -> int:
    time.sleep(delay_seconds)
    return value


def main() -> None:
    ray.init(num_cpus=3)
    try:
        pending = [
            delayed_value.remote(1, 0.15),
            delayed_value.remote(2, 0.05),
            delayed_value.remote(3, 0.10),
        ]
        completion_order = []

        while pending:
            ready, pending = ray.wait(pending, num_returns=1)
            completion_order.append(ray.get(ready[0]))

        assert sorted(completion_order) == [1, 2, 3]
        print(completion_order)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
