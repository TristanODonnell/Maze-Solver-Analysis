# analyzer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List
from src.maze import Maze, OPEN, WALL, DIRECTIONS

@dataclass(frozen=True)
class MazeFeatures:
    cells_total: int
    open_cells: int
    wall_cells: int
    open_ratio: float
    dead_ends: int
    dead_end_ratio: float




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


    dead_ends = 0

    for y in range(maze.height):
        for x in range(maze.width):

            if maze.grid[y][x] != OPEN:
                continue

            open_neighbor_count = 0

            for (dx, dy) in DIRECTIONS:
                nx = x + dx
                ny = y + dy

                if not maze.in_bounds((nx, ny)):
                    continue

                if maze.grid[ny][nx] == OPEN:
                    open_neighbor_count += 1

            if open_neighbor_count == 1:
                dead_ends += 1


    if open_cells == 0:
        dead_end_ratio = 0.0
    else:
        dead_end_ratio = dead_ends/open_cells





    return MazeFeatures(
        cells_total=cells_total,
        open_cells=open_cells,
        wall_cells=wall_cells,
        open_ratio=open_ratio,
        dead_ends=dead_ends,
        dead_end_ratio=dead_end_ratio
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

    if f.dead_ends < 0:
        warnings.append("dead_ends < 0 (impossible)")

    if f.dead_ends > f.open_cells:
        warnings.append("dead_ends > open_cells (impossible)")

    if f.dead_end_ratio < 0 or f.dead_end_ratio > 1:
        warnings.append("dead_end_ratio outside [0, 1]")

    return warnings

def print_features(f: MazeFeatures, warnings: List[str] ) -> None:
    print(
        f"cells_total: {f.cells_total}, "
        f"open_cells: {f.open_cells}, "
        f"wall_cells: {f.wall_cells}, "
        f"open_ratio: {f.open_ratio:.3f}"
    )
    print()
    print(
        f"dead_ends: {f.dead_ends}, "
        f"dead_end_ratio: {f.dead_end_ratio:.3f}"
    )

    for w in warnings:
        print(w)
        print()







