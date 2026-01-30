# labeling.py

from typing import List
from src.eval.metrics import SolverRunMetrics


def choose_oracle_label(metrics: List[SolverRunMetrics]) -> str:
    solved_only = [m for m in metrics if m.solved]

    if len(solved_only) == 0:
        return "NONE"

    solved_only.sort(key=lambda m: (m.nodes_expanded, m.runtime_ms, m.path_length))

    return solved_only[0].solver_name

def compute_regret(
        selected_solver: str,
        oracle_solver: str,
        metrics: List[SolverRunMetrics]
)-> float:

    if oracle_solver == "NONE":
        return 0.0

    selected = next(m for m in metrics if m.solver_name == selected_solver)
    oracle = next(m for m in metrics if m.solver_name == oracle_solver)

    if not selected.solved:
        return 1e9

    return selected.nodes_expanded - oracle.nodes_expanded

