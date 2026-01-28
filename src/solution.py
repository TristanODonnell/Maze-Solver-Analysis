# solution.py

from dataclasses import dataclass
from src import maze
@dataclass
class Solution:
    found: bool
    path: list[maze.coord]
    expanded_count: int
    visited_count: int
    max_frontier: int
    path_length: int

