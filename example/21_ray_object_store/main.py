"""演示使用 ray.put() 在任务间共享只读对象。"""

import ray


@ray.remote
def lookup(database: dict[str, str], key: str) -> str:
    return database[key]


def main() -> None:
    ray.init()
    try:
        database_ref = ray.put({"ray": "distributed", "kubernetes": "cluster"})
        result = ray.get(lookup.remote(database_ref, "ray"))
        assert result == "distributed"
        print(result)
    finally:
        ray.shutdown()


if __name__ == "__main__":
    main()
