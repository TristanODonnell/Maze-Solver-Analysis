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

from collections import deque, defaultdict
from typing import Dict, Optional, List
import heapq

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





def solve_dfs( m: maze.Maze) -> solution.Solution:
    start = m.start
    goal = m.end

    stack: deque[maze.coord] = deque([start])
    came_from: Dict[maze.coord, Optional[maze.coord]] = {start: None}
    visited: set[maze.coord] = {start}

    expanded_count = 0
    max_frontier = len(stack)

    while stack:
        max_frontier = max(max_frontier, len(stack))

        current = stack.pop()
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
                stack.append(neighbor)

    #No path found
    return solution.Solution(
        found=False,
        path=[],
        path_length=0,
        visited_count=len(visited),
        expanded_count=expanded_count,
        max_frontier=max_frontier
    )


def solve_astar( m: maze.Maze) -> solution.Solution:
    start = m.start
    goal = m.end

    # heap of (f_score, tie_breaker, node)
    open_set: list[tuple[float, int, maze.coord]] = []
    tie = 0

    came_from: Dict[maze.coord, Optional[maze.coord]] = {start: None}

    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0.0


    closed: set[maze.coord] = set()
    seen: set[maze.coord] = {start}

    heapq.heappush(open_set, (h(start, goal), tie, start))
    tie += 1

    expanded_count = 0
    max_frontier = len(open_set)

    while open_set:
        max_frontier = max(max_frontier, len(open_set))

        f, _, current = heapq.heappop(open_set)
        expanded_count += 1

        # skip stale entries
        if current in closed:
            continue

        if m.is_goal(current):
            path = reconstruct_path(came_from, goal=current)
            return solution.Solution(
                found=True,
                path=path,
                path_length=len(path) - 1,
                expanded_count=expanded_count,
                visited_count = len(seen),
                max_frontier = max_frontier,
            )

        closed.add(current)

        for neighbor in m.neighbors(current):
            tentative_g = g_score[current] + 1.0  # move cost = 1

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_neighbor = tentative_g + h(neighbor, goal)
                heapq.heappush(open_set, ((f_neighbor), tie, neighbor))
                tie += 1

                seen.add(neighbor)


    #No path found
    return solution.Solution(
        found=False,
        path=[],
        path_length=0,
        visited_count=len(seen),
        expanded_count=expanded_count,
        max_frontier=max_frontier
    )

def h(a: maze.coord, b: maze.coord) -> int:
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)