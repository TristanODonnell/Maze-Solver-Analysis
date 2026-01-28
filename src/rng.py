# rng.py
from __future__ import annotations
from random import Random

rng = Random()

def seed(value: int) -> None:
    rng.seed(value)
