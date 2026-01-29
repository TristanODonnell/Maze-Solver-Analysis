from __future__ import annotations

import copy
import csv
import json
from dataclasses import dataclass, asdict
from hashlib import sha256
from time import perf_counter
from typing import Callable, List, Tuple, Any

from src.maze import coord, Maze
from src import runner


@dataclass
class SolverResult:
    solver_name: str
    solved: bool
    path: List[coord] | None
    path_length: int | None
    expanded_nodes: int
    runtime_ms: float
    notes: str | None


@dataclass
class BenchmarkRow:
    run_id: str
    width: int
    height: int
    family: str
    seed_value: int | None
    density: float | None
    maze_hash: str
    solver_name: str
    solved: bool
    path_length: int | None
    expanded_nodes: int
    runtime_ms: float
    is_best: bool
    best_reason: str


def benchmark(
    configs: List[dict],
    solvers: List[Callable],
    repeats_per_config: int = 1,
    tie_breakers: List[str] = ["solved", "path_length", "runtime_ms"],
    export_path: str | None = None,
    verbose: bool = False,
) -> List[BenchmarkRow]:
    rows: List[BenchmarkRow] = []

    for cfg in configs:
        for r in range(repeats_per_config):
            run_id = make_run_id(cfg, repeat_index=r)

            maze = runner.run_config(cfg)
            mh = compute_maze_hash(maze)

            solver_results: List[SolverResult] = []
            for solver in solvers:
                solver_results.append(run_single_solver(solver, maze, run_id, verbose))

            best_solver_name, best_reason = select_best(solver_results, tie_breakers)

            for result in solver_results:
                is_best = (result.solver_name == best_solver_name)

                row = BenchmarkRow(
                    run_id=run_id,
                    width=cfg["width"],
                    height=cfg["height"],
                    family=cfg["family"],
                    seed_value=cfg.get("seed_value"),
                    density=cfg.get("density"),
                    maze_hash=mh,
                    solver_name=result.solver_name,
                    solved=result.solved,
                    path_length=result.path_length,
                    expanded_nodes=result.expanded_nodes,
                    runtime_ms=result.runtime_ms,
                    is_best=is_best,
                    best_reason=(best_reason if is_best else ""),
                )
                rows.append(row)

            if verbose:
                print_run_summary(run_id, cfg, solver_results, best_solver_name, best_reason)

    if export_path is not None:
        write_rows(rows, export_path)

    return rows


# --------------------
# Helpers
# --------------------

def make_run_id(cfg: dict, repeat_index: int) -> str:
    w = cfg["width"]
    h = cfg["height"]
    fam = cfg["family"]
    seed = cfg.get("seed_value")
    dens = cfg.get("density")
    return f"{fam}_{w}x{h}_seed{seed}_dens{dens}_r{repeat_index}"


def compute_maze_hash(maze: Maze) -> str:
    serialized_bytes = serialize_maze(maze)
    digest_hex = sha256(serialized_bytes).hexdigest()
    return digest_hex[:16]  # 12–16 is fine; pick 16


def serialize_maze(maze: Maze) -> bytes:
    parts: List[str] = []
    parts.append(f"{maze.width}x{maze.height}")
    parts.append(f"S{maze.start}-E{maze.end}")

    for row in maze.grid:
        # handle common grid shapes
        if isinstance(row, str):
            row_str = row
        else:
            # assume iterable of ints/chars
            row_str = "".join(str(cell) for cell in row)
        parts.append(row_str)

    big_str = "\n".join(parts)
    return big_str.encode("utf-8")


def maybe_clone(maze: Maze) -> Maze:
    return copy.deepcopy(maze)


def get_solver_name(solver: Callable) -> str:
    return getattr(solver, "__name__", str(solver))


def normalize_solver_output(raw: Any) -> Tuple[List[coord] | None, int, str | None]:
    # None => unsolved
    if raw is None:
        return None, 0, "returned None"

    # tuple/list forms
    if isinstance(raw, (tuple, list)):
        if len(raw) == 0:
            return None, 0, "empty return"
        if len(raw) == 1:
            return raw[0], 0, None
        if len(raw) == 2:
            return raw[0], int(raw[1]), None
        # len >= 3
        return raw[0], int(raw[1]), str(raw[2]) if raw[2] is not None else None

    # otherwise treat as path
    return raw, 0, None


def run_single_solver(solver: Callable, maze: Maze, run_id: str, verbose: bool) -> SolverResult:
    solver_name = get_solver_name(solver)
    maze_for_solver = maybe_clone(maze)

    t0 = perf_counter()
    try:
        raw = solver(maze_for_solver)
        path, expanded_nodes, notes = normalize_solver_output(raw)

        solved = (path is not None and len(path) > 0)
        path_length = len(path) if solved else None

    except Exception as e:
        path = None
        solved = False
        path_length = None
        expanded_nodes = 0
        notes = f"exception: {e!r}"

    t1 = perf_counter()
    runtime_ms = (t1 - t0) * 1000.0

    if verbose:
        print(f"{run_id} | {solver_name} | solved={solved} len={path_length} expanded={expanded_nodes} ms={runtime_ms:.2f} notes={notes}")

    return SolverResult(
        solver_name=solver_name,
        solved=solved,
        path=path,
        path_length=path_length,
        expanded_nodes=expanded_nodes,
        runtime_ms=runtime_ms,
        notes=notes,
    )


def select_best(results: List[SolverResult], tie_breakers: List[str]) -> Tuple[str, str]:
    if not results:
        return "", "no results"

    def score(r: SolverResult) -> tuple:
        parts = []
        for breaker in tie_breakers:
            if breaker == "solved":
                parts.append(0 if r.solved else 1)  # solved wins
            elif breaker == "path_length":
                parts.append(r.path_length if r.path_length is not None else float("inf"))
            elif breaker == "expanded_nodes":
                parts.append(r.expanded_nodes)
            elif breaker == "runtime_ms":
                parts.append(r.runtime_ms)
            else:
                parts.append(0)
        return tuple(parts)

    best = min(results, key=score)

    if best.solved:
        reason = "best by " + " > ".join(tie_breakers)
    else:
        reason = "none solved; best by " + " > ".join(tie_breakers)

    return best.solver_name, reason


def print_run_summary(run_id: str, cfg: dict, results: List[SolverResult], best_name: str, best_reason: str) -> None:
    print(f"\nRUN {run_id} cfg={cfg}")
    print(f"BEST {best_name} ({best_reason})")
    for r in results:
        print(f"  {r.solver_name:20s} solved={r.solved} len={r.path_length} expanded={r.expanded_nodes} ms={r.runtime_ms:.2f} notes={r.notes}")


def write_rows(rows: List[BenchmarkRow], export_path: str) -> None:
    if export_path.endswith(".csv"):
        write_csv(rows, export_path)
    elif export_path.endswith(".jsonl"):
        write_jsonl(rows, export_path)
    else:
        raise ValueError("unsupported export format (use .csv or .jsonl)")


def write_csv(rows: List[BenchmarkRow], path: str) -> None:
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_jsonl(rows: List[BenchmarkRow], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(asdict(row)) + "\n")
