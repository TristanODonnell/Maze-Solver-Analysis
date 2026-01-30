# run_analyze.py
from src.analyzer import analyze_maze, validate_features, print_features
from tests.helpers import maze_from_ascii

def main():
    maze = maze_from_ascii([
        "S#E",
        ".#.",
    ])

    features = analyze_maze(maze)
    warnings = validate_features(features)

    print_features(features, warnings)

    assert features.open_cells == 4
    assert features.dead_ends == 4
    assert features.shortest_path_length is None
    assert features.reachable_open_cells_from_start == 2
    assert abs(features.reachable_ratio - 0.5) < 1e-9
if __name__ == "__main__":
    main()



