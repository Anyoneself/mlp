"""演示对指定应用异常执行 Ray Task 重试。"""

import ray


class TransientError(RuntimeError):
    pass


@ray.remote
class AttemptTracker:
    def __init__(self) -> None:
        self.attempts = 0

    def next_attempt(self) -> int:
        self.attempts += 1
        return self.attempts


@ray.remote(max_retries=1, retry_exceptions=[TransientError])
def flaky_task(tracker: ray.actor.ActorHandle) -> str:
    attempt = ray.get(tracker.next_attempt.remote())
    if attempt == 1:
        raise TransientError("temporary failure")
    return f"succeeded on attempt {attempt}"


def main() -> None:
    ray.init()
    try:
        tracker = AttemptTracker.remote()
        result = ray.get(flaky_task.remote(tracker))
        assert result == "succeeded on attempt 2"
        print(result)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
