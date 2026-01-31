# eval_heuristic_vs_oracle.py

from __future__ import annotations

import copy
from typing import List, Dict, Tuple

from src.runner import run_config
from src.analyzer import analyze_maze
from src.selectors.heuristic_selector import select_solver_heuristic
from src.eval.metrics import MazeMeta, run_solver_with_metrics
from src.eval.labeling import choose_oracle_label, compute_regret
from src.solvers import solve_bfs, solve_dfs, solve_astar


SOLVERS = [
    ("BFS", solve_bfs),
    ("DFS", solve_dfs),
    ("ASTAR", solve_astar),
]

def build_configs(n: int)-> List[dict]:
    configs = []

    for i in range(n):
        if i % 2 == 0:
            cfg = {
                "width": 21,
                "height": 21,
                "family": "A",
                "seed_value": i,
            }
        else:
            cfg = {
                "width": 21,
                "height": 21,
                "family": "B",
                "seed_value": i,
                "open_ratio": 0.30,
            }
        configs.append(cfg)
    return configs


def main():
    batch_size = 30
    configs = build_configs(batch_size)

    total = 0
    correct = 0
    regrets: List[float] = []
    worst_regret = 0
    none_solved_count = 0

    chose_count = {"BFS": 0, "DFS": 0, "ASTAR": 0}
    oracle_count = {"BFS": 0, "DFS": 0, "ASTAR": 0, "NONE": 0}
    match_count = {"BFS": 0, "DFS": 0, "ASTAR": 0}  # matches by predicted label

    for idx, cfg in enumerate(configs):
        total += 1

        maze = run_config(cfg)
        f = analyze_maze(maze)

        predicted = select_solver_heuristic(f)
        chose_count[predicted] += 1

        # Build meta (seed must be int)
        seed_val = cfg.get("seed_value")
        seed_int = seed_val if seed_val is not None else 0

        meta = MazeMeta(
            maze_id=f"run_{idx}",
            seed=seed_int,
            family=cfg["family"],
            width=cfg["width"],
            height=cfg["height"],
            open_ratio=cfg.get("open_ratio"),
        )

        metrics_list = []
        for (solver_name, solver_fn) in SOLVERS:
            maze_copy = copy.deepcopy(maze)
            m = run_solver_with_metrics(
                maze_copy,
                solver_fn,
                solver_name=solver_name,
                meta=meta
            )
            metrics_list.append(m)
            print(solver_name, "->",
                  "SOLVED?", getattr(m, "solved", None),
                  "PATHLEN", getattr(m, "path_length", None),
                  "EXPANDED", getattr(m, "expanded", None),
                  "MS", getattr(m, "ms", None),
                  "ERR", getattr(m, "error", None))

        oracle = choose_oracle_label(metrics_list)
        oracle_count[oracle] += 1

        if oracle == "NONE":
            none_solved_count += 1
            continue

        if predicted == oracle:
            correct += 1
            match_count[predicted] += 1

        r = compute_regret(predicted, oracle, metrics_list)
        regrets.append(r)
        if r > worst_regret:
            worst_regret = float(r)

    scored = total - none_solved_count
    accuracy = (correct / scored) if scored else 0.0
    avg_regret = (sum(regrets) / len(regrets)) if regrets else 0.0

    print(f"accuracy: {accuracy:.3f}")
    print(f"avg_regret_expanded: {avg_regret:.2f}")
    print(f"worst_regret_expanded: {worst_regret:.2f}")
    print(f"none_solved_count: {none_solved_count}")
    print()
    print(f"chose_count: {chose_count}")
    print(f"oracle_count: {oracle_count}")
    print(f"match_count: {match_count}")

if __name__ == "__main__":
    main()