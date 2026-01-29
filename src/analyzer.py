# analyzer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from src.maze import Maze

@dataclass(frozen=True)
class MazeFeatures:
    pass


def analyze_maze(maze: Maze)-> MazeFeatures:
    maze.validate()

    maze_features = MazeFeatures()

    return maze_features

def validate_features(features: MazeFeatures) -> List[str]:
    warnings = []

    return warnings



