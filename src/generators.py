# generators.py
from src import maze
from src.rng import rng as prng

from collections import deque
from typing import List


import numpy as np

def manhattan_distance_numpy(point1, point2):
    """
    Calculates the Manhattan distance between two NumPy arrays.
    """
    point1_arr = np.array(point1)
    point2_arr = np.array(point2)
    return np.sum(np.abs(point1_arr - point2_arr))

def create_grid(width: int, height: int) -> List[List[int]]:
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(maze.WALL)
        grid.append(row)

    return grid

def create_maze(grid, start, end) -> maze.Maze:


    width = get_width(grid)
    height = get_height(grid)

    sx, sy = start
    ex, ey = end

    grid[sy][sx] = maze.OPEN
    grid[ey][ex] = maze.OPEN
    created = maze.Maze(width, height, grid, start, end)

    created.validate()
    return created

# perfect maze
def generate_perfect(grid: List[List[int]], start: maze.coord, end: maze.coord) -> List[List[int]]:
    start_cell = snap_to_odd_interior(grid, start)
    end_cell   = snap_to_odd_interior(grid, end)

    width = get_width(grid)
    height = get_height(grid)

    def is_cell(pos):
        x, y = pos
        return (
            0 < x < width - 1
            and 0 < y < height - 1
            and x % 2 == 1
            and y % 2 == 1
        )

    def neighbors_2_steps(pos):
        x, y = pos
        results = []
        for dx, dy in maze.DIRECTIONS:
            nx, ny = x + 2 * dx, y + 2 * dy
            if is_cell((nx, ny)):
                results.append((nx, ny))
        return results

    stack = [start_cell]
    visited = {start_cell}

    grid[start_cell[1]][start_cell[0]] = maze.OPEN

    while stack:
        cx, cy = stack[-1]

        unvisited = [n for n in neighbors_2_steps((cx, cy)) if n not in visited]
        if not unvisited:
            stack.pop()
            continue

        nx, ny = prng.choice(unvisited)

        # carve wall between cells
        wx = (cx + nx) // 2
        wy = (cy + ny) // 2
        grid[wy][wx] = maze.OPEN
        grid[ny][nx] = maze.OPEN

        visited.add((nx, ny))
        stack.append((nx, ny))

    # ensure end is open on a real cell coordinate (connected in perfect-maze space)
    ex, ey = end_cell
    grid[ey][ex] = maze.OPEN

    return grid

def generate_dense_solvable(grid, start, end, open_ratio: float) -> List[List[int]]:

    #clamps
    if open_ratio< 0.0:
        open_ratio = 0.0
    if open_ratio > 1.0:
        open_ratio = 1.0

    target_open = int(open_ratio * (get_width(grid) * get_height(grid)))
    
    path_cells = carve_path_start_to_end(grid, start, end)
    for cell in path_cells:
        cx = cell[0]
        cy = cell[1]
        grid[cy][cx] = maze.OPEN

    while count_open_cells(grid) < target_open:
        candidate = random_cell_position(grid)
        cx = candidate[0]
        cy = candidate[1]
        if grid[cy][cx] == maze.OPEN:
            continue

        open_nbrs = count_open_neighbors(grid, candidate)

        if open_nbrs == 0:
            continue


        grid[cy][cx] = maze.OPEN

    if not is_solvable(grid, start, end):
        fresh = create_grid(get_width(grid), get_height(grid))
        return generate_dense_solvable(fresh, start, end, open_ratio)

    return grid

def random_cell_position(grid) -> tuple :
    width = get_width(grid)
    height = get_height(grid)
    x = prng.randrange(width)
    y = prng.randrange(height)
    return x, y

def count_open_cells(grid) -> int :
    count = 0
    for y in range(get_height(grid)):
        for x in range(get_width(grid)):
            if grid[y][x] == maze.OPEN:
                count += 1
    return count

def count_open_neighbors(grid, cell: tuple) -> int:
    x, y = cell
    count = 0
    for dx, dy in maze.DIRECTIONS:
        nx, ny = x + dx, y + dy
        neighbor = (nx, ny)
        if in_bounds(grid, neighbor) and grid[ny][nx] == maze.OPEN:
            count += 1
    return count

def carve_path_start_to_end(grid, start, end) -> List[tuple]:
    current = start
    path = [start]
    visited = {start}

    while current != end:
        neighbors = []
        cx, cy = current

        for dx, dy in maze.DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            neighbor = (nx, ny)
            if in_bounds(grid, neighbor):
                neighbors.append(neighbor)

        better = []


        for n in neighbors:
            if manhattan_distance_numpy(n, end) < manhattan_distance_numpy(current, end):
                better.append(n)

        if better and prng.random() < 0.85:
            nxt = prng.choice(better)
        else:
            nxt = prng.choice(neighbors)



        if nxt in visited:
            unvisited = [n for n in neighbors if n not in visited]
            if unvisited:
                 nxt = prng.choice(unvisited)

        current = nxt
        path.append(current)
        visited.add(current)

    return path

def is_solvable(grid, start, end) -> bool:

    q = deque([start])
    visited = {start}

    while q:
        x, y = q.popleft()
        if (x, y) == end:
            return True

        for dx, dy in maze.DIRECTIONS:
            nx, ny = x + dx, y + dy
            n = (nx, ny)
            if not in_bounds(grid, n) or n in visited:
                continue

            if n != end and grid[ny][nx] != maze.OPEN:
                continue

            visited.add(n)
            q.append(n)

    return False



def in_bounds(grid, pos) -> bool:
    x, y = pos
    height = get_height(grid)
    width = get_width(grid)
    return 0 <= x < width and 0 <= y < height

def get_height(grid) -> int: return len(grid)
def get_width(grid) -> int: return len(grid[0])

def snap_to_odd_interior(grid, pos: tuple[int, int]) -> tuple[int, int]:
    w = get_width(grid)
    h = get_height(grid)
    x, y = pos

    # clamp to interior (avoid boundary walls)
    x = min(max(1, x), w - 2)
    y = min(max(1, y), h - 2)

    # force odd coordinates (cell centers)
    if x % 2 == 0:
        x = x - 1 if x > 1 else x + 1
    if y % 2 == 0:
        y = y - 1 if y > 1 else y + 1

    return x, y





