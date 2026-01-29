# run_benchmark.py
from src.benchmark import benchmark
from src import config
from src.solvers import solve_bfs, solve_dfs, solve_astar

def main():
    configs = [
        config.PRESETS["a_small"],
        config.PRESETS["b_medium"],
    ]

    solvers = [
        solve_bfs,
        solve_dfs,
        solve_astar,
    ]

    benchmark(
        configs=configs,
        solvers=solvers,
        repeats_per_config=3,
        verbose=True,
        export_path="benchmark_results.csv",
    )

if __name__ == "__main__":
    main()