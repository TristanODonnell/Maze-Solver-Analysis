# analyzer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from src.maze import Maze, OPEN, WALL

@dataclass(frozen=True)
class MazeFeatures:
    cells_total: int
    open_cells: int
    wall_cells: int
    open_ratio: float



def analyze_maze(maze: Maze)-> MazeFeatures:
    maze.validate()

    cells_total = maze.width * maze.height

    open_cells = 0
    wall_cells = 0

    for row in maze.grid:
        for cell in row:
            if cell == OPEN:
                open_cells += 1
            elif cell == WALL:
                wall_cells += 1
            else:
                raise ValueError(f"Invalid/Unknown cell value: {cell!r} ")

    open_ratio = open_cells / cells_total


    return MazeFeatures(
        cells_total=cells_total,
        open_cells=open_cells,
        wall_cells=wall_cells,
        open_ratio=open_ratio,
    )

def validate_features(f: MazeFeatures) -> List[str]:
    warnings = []

    if f.cells_total <= 0:
        warnings.append("Cells total less than or equal to 0")

    if f.open_cells + f.wall_cells != f.cells_total:
        warnings.append(
            "Open and wall cells do not equal total cells"
        )

    if f.open_ratio < 0 or f.open_ratio > 1:
        warnings.append(
            "open_ratio outside [0, 1]"
        )

    return warnings



