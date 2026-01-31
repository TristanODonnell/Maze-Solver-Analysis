# src/eval/metrics.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional
import time

from src import maze as maze_mod
from src import solution as solution_mod


@dataclass(frozen=True)
class MazeMeta:
    maze_id: str
    seed: int
    family: str   # "A" or "B"
    width: int
    height: int
    open_ratio: Optional[float] = None


@dataclass(frozen=True)
class SolverRunMetrics:
    # --- maze identity / params ---
    maze_id: str
    seed: int
    family: str
    width: int
    height: int
    open_ratio: Optional[float]

    # --- solver identity ---
    solver_name: str   # "BFS" | "DFS" | "ASTAR"

    # --- outcomes ---
    solved: bool
    path_length: int
    nodes_expanded: int
    visited_count: int
    max_frontier: int
    runtime_ms: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_solver_with_metrics(
    m: maze_mod.Maze,
    solver_fn: Callable[[maze_mod.Maze], solution_mod.Solution],
    *,
    solver_name: str,
    meta: MazeMeta,
) -> SolverRunMetrics:
    t0 = time.perf_counter()
    sol = solver_fn(m)
    runtime_ms = (time.perf_counter() - t0) * 1000.0

    return SolverRunMetrics(
        maze_id=meta.maze_id,
        seed=meta.seed,
        family=meta.family,
        width=meta.width,
        height=meta.height,
        open_ratio=meta.open_ratio,
        solver_name=solver_name,
        solved=sol.found,
        path_length=sol.path_length,
        nodes_expanded=sol.expanded_count,
        visited_count=sol.visited_count,
        max_frontier=sol.max_frontier,
        runtime_ms=runtime_ms,
    )