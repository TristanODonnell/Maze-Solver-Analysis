# heuristic_selector.py

from src.analyzer import MazeFeatures

"""
Rules:
Rule 1 (Tiny maze):
If width * height <= 225 → DFS

Rule 2 (Low reachability):
If reachable_ratio < 0.90 → BFS

Rule 3 (Open + low dead ends):
If open_ratio >= 0.40 AND dead_end_ratio <= 0.15 → ASTAR

Rule 4 (Very dead-end heavy):
If dead_end_ratio >= 0.35 → BFS

Default:
ASTAR
"""

def select_solver_heuristic(f: MazeFeatures) -> str:

    # Rule 1: Tiny maze → DFS (contrast)
    if f.cells_total <= 225:
        return "DFS"

    # Rule 2: Very low reachability → BFS
    if f.reachable_ratio < 0.90:
        return "BFS"

    # Rule 3: Moderately open + low dead ends → A*
    if f.open_ratio >= 0.40 and f.dead_end_ratio <= 0.15:
        return "ASTAR"

    # Rule 4: Very dead-end heavy → BFS
    if f.dead_end_ratio >= 0.35:
        return "BFS"

    # Default
    return "ASTAR"
