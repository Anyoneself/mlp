"""演示使用 Placement Group 原子预留任务资源。"""

import ray
from ray.util.placement_group import placement_group, remove_placement_group
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy


@ray.remote(num_cpus=1)
def run_in_bundle() -> str:
    return "completed"


def main() -> None:
    ray.init(num_cpus=2)
    group = None
    try:
        group = placement_group([{"CPU": 1}, {"CPU": 1}], strategy="PACK")
        ray.get(group.ready(), timeout=10)

        refs = [
            run_in_bundle.options(
                scheduling_strategy=PlacementGroupSchedulingStrategy(
                    placement_group=group,
                    placement_group_bundle_index=index,
                )
            ).remote()
            for index in range(2)
        ]
        results = ray.get(refs)
        assert results == ["completed", "completed"]
        print("placement group tasks completed")
    finally:
        if group is not None:
            remove_placement_group(group)
        ray.shutdown()


if __name__ == "__main__":
    main()
