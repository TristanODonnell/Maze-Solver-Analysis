# heuristic_selector.py

from src.analyzer import MazeFeatures


def select_solver_heuristic(f: MazeFeatures) -> str:
    # tiny mazes: DFS is fine
    if f.cells_total <= 225:
        return "DFS"

    # very open mazes (often perfect-maze-like corridors): DFS tends to expand less
    if f.open_ratio >= 0.35:
        return "DFS"

    # if lots of dead ends, BFS can be safer (more systematic)
    if f.dead_end_ratio >= 0.20:
        return "BFS"

    # otherwise pick A*
    return "ASTAR"
