# Baselines

## Heuristic Selector v1 (2026-01-30)
Dataset:
- batch_size: 30
- size: 21x21
- families: A (seeds even), B (seeds odd, open_ratio=0.30)

Heuristic rules:
- DFS if cells_total <= 225
- DFS if open_ratio >= 0.35
- BFS if dead_end_ratio >= 0.20
- else ASTAR

Oracle metric:
- minimize expanded nodes (solved-only)

Results:
- accuracy: 0.467
- avg_regret_expanded: 16.47
- worst_regret_expanded: 62.00
- none_solved_count: 0
- chose_count: ...
- oracle_count: ...
- match_count: ...


Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

(.venv) PS C:\Users\trist\PycharmProjects\Maze-Solver-Analysis> python -m scripts.eval_heuristic_vs_oracle
BFS -> SOLVED? True PATHLEN 64 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 64 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 64 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 44 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 52 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 52 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 52 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 56 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 56 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 56 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 58 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 60 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 60 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 60 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 42 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 54 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 76 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 76 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 76 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 46 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 44 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 60 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 60 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 60 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 48 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 88 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 88 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 88 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 42 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 46 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 42 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 84 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 84 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 84 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 50 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 56 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 56 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 56 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 54 EXPANDED None MS None ERR None
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 100 EXPANDED None MS None ERR None     
DFS -> SOLVED? True PATHLEN 100 EXPANDED None MS None ERR None     
ASTAR -> SOLVED? True PATHLEN 100 EXPANDED None MS None ERR None   
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 44 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 52 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 52 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 52 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 72 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
BFS -> SOLVED? True PATHLEN 92 EXPANDED None MS None ERR None      
DFS -> SOLVED? True PATHLEN 92 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 92 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 50 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
BFS -> SOLVED? True PATHLEN 120 EXPANDED None MS None ERR None     
DFS -> SOLVED? True PATHLEN 120 EXPANDED None MS None ERR None     
ASTAR -> SOLVED? True PATHLEN 120 EXPANDED None MS None ERR None   
BFS -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None
DFS -> SOLVED? True PATHLEN 62 EXPANDED None MS None ERR None      
ASTAR -> SOLVED? True PATHLEN 40 EXPANDED None MS None ERR None    
accuracy: 0.467
avg_regret_expanded: 16.47
worst_regret_expanded: 62.00
none_solved_count: 0

chose_count: {'BFS': 0, 'DFS': 15, 'ASTAR': 15}
oracle_count: {'BFS': 0, 'DFS': 29, 'ASTAR': 1, 'NONE': 0}
match_count: {'BFS': 0, 'DFS': 14, 'ASTAR': 0}
(.venv) PS C:\Users\trist\PycharmProjects\Maze-Solver-Analysis> 