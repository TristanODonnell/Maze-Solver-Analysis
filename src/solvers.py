# solvers
""" found: bool
path: list[coord] (ordered start→end)
path_length: int (len(path)-1)
visited_count: int (how many unique cells visited)
expanded_count: int (how many nodes popped from queue/stack)
max_frontier: int (max size of queue/stack/heap)
runtime_ms (optional)"""

## BFS, DFS, A*
from __future__ import annotations
from collections import deque
from typing import Dict, Optional, List

from src import maze, solution


def solve_bfs( m: maze.Maze) -> solution.Solution:
    start = m.start
    goal = m.end

    queue: deque[maze.coord] = deque([start])

    came_from: Dict[maze.coord, Optional[maze.coord]] = {start: None}
    visited: set[maze.coord] = {start}

    expanded_count = 0
    max_frontier = len(queue)

    while queue:
        max_frontier = max(max_frontier, len(queue))

        current = queue.popleft()
        expanded_count += 1

        if m.is_goal(current):
            path = reconstruct_path(came_from, goal=current)
            return solution.Solution(
                found=True,
                path=path,
                path_length=len(path) - 1,
                expanded_count=expanded_count,
                visited_count = len(visited),
                max_frontier = max_frontier,
            )

        for neighbor in m.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    #No path found
    return solution.Solution(
        found=False,
        path=[],
        path_length=0,
        visited_count=len(visited),
        expanded_count=expanded_count,
        max_frontier=max_frontier
    )

def reconstruct_path(
    came_from: Dict[maze.coord, Optional[maze.coord]],
    goal: maze.coord
) -> List[maze.coord]:
    path: List[maze.coord] = []
    current: Optional[maze.coord] = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path





def solve_dfs(maze) -> solution:
def solve_astar(maze) -> solution:

