# heuristic_selector.py

from src.analyzer import MazeFeatures

def select_solver_heuristic(f: MazeFeatures) -> str:
    return "BFS"