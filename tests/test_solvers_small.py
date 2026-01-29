# test_solvers_small.py

from tests.helpers import maze_from_ascii, assert_valid_path
from src.solvers import solve_bfs, solve_astar, solve_dfs

def test_bfs_finds_path():
    m = maze_from_ascii([
        "S....",
        "###..",
        "...#.",
        "..##.",
        "....E",
    ])

    sol = solve_bfs(m)

    assert sol.found == True
    assert sol.path_length == len(sol.path) - 1

    assert_valid_path(m, sol.path)

def test_astar_matches_bfs_shortest_path():
    m = maze_from_ascii([
        "S....",
        "###..",
        "...#.",
        "..##.",
        "....E",
    ])

    sol_bfs = solve_bfs(m)
    sol_astar = solve_astar(m)

    assert sol_bfs.found
    assert sol_astar.found
    assert sol_astar.path_length == sol_bfs.path_length

def test_dfs_finds_a_path_if_one_exists():
    m = maze_from_ascii([
        "S....",
        "###..",
        "...#.",
        "..##.",
        "....E",
    ])

    sol = solve_dfs(m)

    assert sol.found
    assert_valid_path(m, sol.path)

def test_unsolvable_maze_returns_not_found():
    m = maze_from_ascii([
        "S#E",
        "###",
        "...",
    ])

    sol = solve_bfs(m)

    assert sol.found is False
    assert sol.path == []
    assert sol.path_length == 0
