# test_integration_presets

from src import runner, config, solvers
from src.solvers import solve_bfs, solve_astar, solve_dfs
from tests import helpers

def test_preset_a_small_all_solvers_work():
    m = runner.run_config(config.PRESETS["a_small"], verbose=False)
    sol_bfs = solve_bfs(m)
    sol_astar = solve_astar(m)
    sol_dfs = solve_dfs(m)

    assert sol_bfs.found
    helpers.assert_valid_path(m, sol_bfs.path)
    assert sol_astar.found
    helpers.assert_valid_path(m, sol_astar.path)
    assert sol_dfs.found
    helpers.assert_valid_path(m, sol_dfs.path)
    assert sol_astar.path_length == sol_bfs.path_length
