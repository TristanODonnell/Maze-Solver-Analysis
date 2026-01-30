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
    return "BFS"