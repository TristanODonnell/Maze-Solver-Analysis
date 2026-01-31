# dataset.py

import copy
from dataclasses import asdict
from typing import Callable, List, Tuple

from src.analyzer import analyze_maze
from src.eval.metrics import run_solver_with_metrics, MazeMeta
from src.eval.labeling import choose_oracle_label
from src.runner import run_config


def extract_feature_dict(maze):
    f = analyze_maze(maze)
    feature_dict = asdict(f)
    return feature_dict

def run_all_solvers_with_metrics(
        maze,
        meta,
        solver_fns: List[Tuple[str, Callable]]
):
    metrics_list = []

    for (solver_name, solver_fn) in solver_fns:
        maze_copy = copy.deepcopy(maze)
        m = run_solver_with_metrics(
            maze_copy,
            solver_fn,
            solver_name=solver_name,
            meta=meta,
        )
        metrics_list.append(m)


    return metrics_list

def build_row_for_maze(
        maze,
        meta,
        solver_fns: List[Tuple[str, Callable]]
):
    features = extract_feature_dict(maze)
    metrics_list = run_all_solvers_with_metrics(maze, meta, solver_fns)
    label = choose_oracle_label(metrics_list)

    if features["shortest_path_length"] is None:
        features["shortest_path_length"] = -1

    meta_dict = asdict(meta)
    if "open_ratio" in meta_dict:
        del meta_dict["open_ratio"]

    row = dict(features)
    row.update(meta_dict)
    row["label"] = label

    return row, metrics_list

def build_dataset(configs, solver_fns):
    rows = []
    metrics_lookup = {}

    for cfg in configs:
        maze, meta = build_maze_and_meta(cfg)
        row, metrics_list = build_row_for_maze(maze, meta, solver_fns)

        rows.append(row)
        metrics_lookup[meta.maze_id] = metrics_list

    return rows, metrics_lookup


def build_maze_and_meta(cfg):
    maze = run_config(cfg, verbose=False)

    maze_id = make_id_from_cfg(cfg)

    meta = MazeMeta(
        maze_id=maze_id,
        seed=cfg["seed_value"],
        family=cfg["family"],
        width=cfg["width"],
        height=cfg["height"],
        open_ratio=cfg.get("open_ratio")
    )

    return maze, meta

def make_id_from_cfg(cfg):
    return f"{cfg['family']}_{cfg['width']}x{cfg['height']}_seed{cfg['seed_value']}_r{cfg.get('open_ratio')}"


