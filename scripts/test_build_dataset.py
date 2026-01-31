# test_build_dataset.py

import copy
from collections import Counter

from src.config import PRESETS
from src.solvers import solve_bfs, solve_dfs, solve_astar
from src.ml.dataset import build_dataset


def main():
    solver_fns = [
        ("BFS", solve_bfs),
        ("DFS", solve_dfs),
        ("ASTAR", solve_astar),
    ]

    configs = []
    for preset in PRESETS.values():
        for open_ratio in [0.20, 0.35, 0.50, 0.65]:
            if preset["family"] == "B":
                for i in range(3):
                    cfg = copy.deepcopy(preset)
                    cfg["open_ratio"] = open_ratio
                    cfg["seed_value"] = preset.get("seed_value", 0) + i
                    configs.append(cfg)


    rows, metrics_lookup = build_dataset(configs, solver_fns)

    print("num rows:", len(rows))
    assert len(rows) == len(configs)

    print("row keys:", rows[0].keys())

    labels = [row["label"] for row in rows]
    print("label counts:", Counter(labels))

    for row in rows:
        assert "label" in row
        assert row["label"] is not None

        for k, v in row.items():
            if k != "label":
                assert v is not None, f"{k} is None"

    print("Dataset smoke test passed.")


if __name__ == "__main__":
    main()