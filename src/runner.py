# runner.py
#orchestration for maze generation/construction tied to parameters

from src import generators, maze
from src.rng import seed

def run_config(cfg: dict, *, verbose: bool = False) -> maze.Maze:
    return run(**cfg, verbose=verbose)

def run(width: int,
        height: int,
        family: str,
        seed_value: int | None = None,
        open_ratio: float | None = None,
        *,
        verbose: bool = True,
    ) -> maze.Maze:
    # ---- validation ----
    if width <= 0 or height <= 0:
        raise ValueError(f"width/height must be positive, got {width}x{height}")

    family = family.upper().strip()
    if family not in {"A", "B"}:
        raise ValueError(f"Unknown family={family!r}. Expected 'A' or 'B'.")

    # ---- seeding (once, here) ----
    if seed_value is not None:
        seed(seed_value)

    built_grid = generators.create_grid(width, height)
    start = (0, 0)
    end = (width - 1, height - 1)

    if family == "A":
        # critical: make Maze endpoints match the perfect-maze cell lattice
        start = generators.snap_to_odd_interior(built_grid, start)
        end = generators.snap_to_odd_interior(built_grid, end)

        generators.generate_perfect(built_grid, start, end)
    elif family == "B":
        if open_ratio is None:
             raise ValueError("Family B requires open_ratio (e.g., 0.25).")
        if not (0.0 <= open_ratio <= 1.0):
            raise ValueError(f"open_ratio must be in [0.0, 1.0], got {open_ratio}")

        generators.generate_dense_solvable(
            grid=built_grid,
            start=start,
            end=end,
            open_ratio=open_ratio,
        )
    maze_created = generators.create_maze(built_grid, start, end)

    if verbose:
        print(
            f"[run] family={family} width={width} height={height} "
            f"seed={seed_value} open_ratio={open_ratio}"
        )
        maze_created.display()

    return maze_created

if __name__ == "__main__":
    from src import config
    run_config(config.DEFAULT)

