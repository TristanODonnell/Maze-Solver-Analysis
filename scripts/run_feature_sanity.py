# run_feature_sanity

from src.analyzer import analyze_maze, validate_features
from src import generators as g
from src import maze, rng



def main():
    rng.seed(42)

    features_list = []
    meta_list = []

    for i in range(30):
        # ---- Family A ----
        width, height = 21, 21
        start = (0, 0)
        end = (width - 1, height - 1)

        grid = g.create_grid(width, height)
        grid = g.generate_perfect(grid, start)
        m = g.create_maze(grid, start, end)

        f = analyze_maze(m)
        warnings = validate_features(f)

        features_list.append(f)
        meta_list.append({"family": "A"})

        # ---- Family B ----
        open_ratio_target = rng.rng.choice([0.15, 0.25, 0.35, 0.45])

        grid = g.create_grid(width, height)
        grid = g.generate_dense_solvable(grid, start, end, open_ratio_target)
        m = g.create_maze(grid, start, end)

        f = analyze_maze(m)
        warnings = validate_features(f)

        features_list.append(f)
        meta_list.append({"family": "B", "open_ratio_target": open_ratio_target})
    print("=== Feature ranges ===")

    def non_none(values):
        return [v for v in values if v is not None]

    print("open_ratio:",
          min(f.open_ratio for f in features_list),
          max(f.open_ratio for f in features_list))

    print("dead_end_ratio:",
          min(f.dead_end_ratio for f in features_list),
          max(f.dead_end_ratio for f in features_list))

    print("reachable_ratio:",
          min(f.reachable_ratio for f in features_list),
          max(f.reachable_ratio for f in features_list))

    spaths = non_none(f.shortest_path_length for f in features_list)
    print("shortest_path_length:",
          min(spaths), max(spaths))

    unsolved = sum(
        1 for f in features_list
        if f.shortest_path_length is None
    )

    print("unsolved mazes:", unsolved, "/", len(features_list))

    pairs = list(zip(features_list, meta_list))
    pairs.sort(key=lambda p: p[0].dead_end_ratio, reverse=True)

    print("\n=== Top 3 by dead_end_ratio ===")
    for f, meta in pairs[:3]:
        print(
            meta,
            "dead_end_ratio=", round(f.dead_end_ratio, 3),
            "open_ratio=", round(f.open_ratio, 3),
            "reachable_ratio=", round(f.reachable_ratio, 3),
            "spath=", f.shortest_path_length,
        )

if __name__ == "__main__":
    main()



