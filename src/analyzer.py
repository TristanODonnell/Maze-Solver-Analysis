# analyzer.py

from __future__ import annotations
import copy
from collections import deque
from dataclasses import dataclass
from typing import List

from src.maze import Maze, OPEN, WALL, DIRECTIONS, coord
from src.solvers import solve_bfs

@dataclass(frozen=True)
class MazeFeatures:
    cells_total: int
    open_cells: int
    wall_cells: int
    open_ratio: float
    dead_ends: int
    dead_end_ratio: float
    shortest_path_length: int | None
    reachable_open_cells_from_start: int
    reachable_ratio: float


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

    reachable = 0
    visited = set()

    queue = deque()

    if maze.is_open(maze.start):
        visited.add(maze.start)
        queue.append(maze.start)
    else:
        raise ValueError("Invalid Maze")

    while queue:
        current = queue.popleft()

        reachable += 1

        for neighbor in maze.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    reachable_open_cells_from_start = reachable

    if open_cells == 0:
        reachable_ratio = 0.0
    else:
        reachable_ratio = reachable_open_cells_from_start /open_cells

    #Dead Ends
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

    #Shortest Path
    bfs_solution = solve_bfs(copy.deepcopy(maze))
    if bfs_solution.found:
        shortest_path_length = bfs_solution.path_length
    else:
        shortest_path_length = None

    return MazeFeatures(
        cells_total=cells_total,
        open_cells=open_cells,
        wall_cells=wall_cells,
        open_ratio=open_ratio,
        dead_ends=dead_ends,
        dead_end_ratio=dead_end_ratio,
        shortest_path_length=shortest_path_length,
        reachable_open_cells_from_start=reachable_open_cells_from_start,
        reachable_ratio=reachable_ratio
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

    if f.reachable_open_cells_from_start < 0:
        warnings.append(
            "reachable_open_cells_from_start < 0 (impossible)"
        )

    if f.reachable_open_cells_from_start > f.open_cells:
        warnings.append(
            "reachable_open_cells_from_start > open_cells (impossible)"
        )

    if f.reachable_ratio < 0 or f.reachable_ratio > 1:
        warnings.append("reach_ratio outside [0, 1]")

    if f.dead_ends < 0:
        warnings.append("dead_ends < 0 (impossible)")

    if f.dead_ends > f.open_cells:
        warnings.append("dead_ends > open_cells (impossible)")

    if f.dead_end_ratio < 0 or f.dead_end_ratio > 1:
        warnings.append("dead_end_ratio outside [0, 1]")

    if f.shortest_path_length is not None:
        if f.shortest_path_length < 1:
            warnings.append("shortest_path_length < 1")

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
        f"reachable_open_cells_from_start: {f.reachable_open_cells_from_start}, reachable_ratio: {f.reachable_ratio:.3f}")
    print()
    print(
        f"dead_ends: {f.dead_ends}, "
        f"dead_end_ratio: {f.dead_end_ratio:.3f}"
    )
    print()
    print(
        f"shortest_path_length: {f.shortest_path_length}"
    )

    for w in warnings:
        print(w)
        print()







