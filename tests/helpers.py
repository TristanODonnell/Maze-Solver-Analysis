# helpers.py
from src.maze import Maze, WALL, OPEN

def maze_from_ascii(lines):
    height = len(lines)
    width = len(lines[0])

    grid = [[WALL for _ in range(width)] for _ in range(height)]
    start = None
    end = None

    for y in range(0, height):
        line = lines[y]
        assert len(line) == width

        for x in range(width):
            ch = line[x]

            if ch == '#':
                grid[y][x] = WALL
            elif ch == '.' or ch == 'S' or ch == 'E':
                grid[y][x] = OPEN

            if ch == 'S': start = (x, y)
            if ch == 'E': end = (x, y)

    assert start is not None and end is not None

    m = Maze(width, height, grid, start, end)
    m.validate()
    return m

def manhattan(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)

def assert_valid_path(m, path):
    assert path is not None
    assert len(path) > 0
    assert path[0] == m.start
    assert path[-1] == m.end

    for a, b in zip(path, path[1:]):
        assert manhattan(a, b) == 1
        assert m.is_open(b)

