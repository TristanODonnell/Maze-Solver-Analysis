# run_analyze.py
from src.analyzer import analyze_maze, validate_features, print_features
from tests.helpers import maze_from_ascii

def main():
    maze = maze_from_ascii([
        "S.E"
    ])

    features = analyze_maze(maze)
    warnings = validate_features(features)

    print_features(features, warnings)

    assert features.dead_ends == 2
    assert features.open_cells == 3
    assert len(warnings) == 0

if __name__ == "__main__":
    main()



