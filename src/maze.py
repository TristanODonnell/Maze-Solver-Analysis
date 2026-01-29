# maze.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List


coord = Tuple[int, int] #coordinate(x,y)

WALL = 1
OPEN = 0

DIRECTIONS = [
    (0, -1),  # up
    (0, 1),   # down
    (-1, 0),  # left
    (1, 0),   # right
]

@dataclass(frozen=True)
class Maze:
    width:int
    height:int
    grid: List[List[int]]
    start: coord
    end: coord

    def in_bounds(self, pos: coord) -> bool:
        x, y = pos
        return (0 <= x < self.width
                and 0 <= y < self.height)

    def is_open(self, pos: coord) -> bool:
        if not self.in_bounds(pos):
            return False
        x, y = pos
        return self.grid[y][x] == OPEN

    def neighbors(self, pos: coord) -> List[coord]:
        x, y = pos
        results = []

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)

            if self.in_bounds(next_pos) and self.is_open(next_pos):
                results.append(next_pos)

        return results


    def validate(self) -> None:
        # Height check: number of rows
        if len(self.grid) != self.height:
            raise ValueError(
                f"Grid height mismatch: len(grid)={len(self.grid)} but height={self.height}"
            )

        for y, row in enumerate(self.grid):
            if len(row) != self.width:
                raise ValueError(
                    f"Grid width mismatch at row y={y}: len(row)={len(row)} but width={self.width}"
                )
        if not self.in_bounds(self.start):
            raise ValueError(f"Start out of bounds: start={self.start}")

        if not self.in_bounds(self.end):
            raise ValueError(f"End out of bounds: end={self.end}")

        # Start / end not walls
        if not self.is_open(self.start):
            raise ValueError(f"Start is not open (wall cell): start={self.start}")

        if not self.is_open(self.end):
            raise ValueError(f"End is not open (wall cell): end={self.end}")


    def is_goal(self, pos: coord) -> bool:
        return pos == self.end

    def display(self, path: set[coord] | list[coord] | None = None) -> None:
        path_set = set(path) if path is not None else set()

        for y in range(self.height) :
            row_chars = []
            for x in range(self.width):
                pos = (x, y)

                if pos == self.start:
                    row_chars.append("S")
                elif pos == self.end:
                    row_chars.append("E")
                elif pos in path_set:
                    row_chars.append("*")
                elif self.grid[y][x] == WALL:
                    row_chars.append("#")
                else:
                    row_chars.append(".")

            print(" ".join(row_chars))

        print()





