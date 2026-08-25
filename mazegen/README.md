# mazegen

A self-contained, seed-reproducible maze generator.

`mazegen` builds a fully connected, always-loopy (Pac-Man-style) maze
(never a single-path "perfect" maze) using Wilson's algorithm followed by
a dead-end-removal pass. It includes a visible "42" pattern near the
center of the grid when the maze is large enough to fit it. It has no
dependencies outside the Python standard library.

## Install

```
pip install mazegen-1.42-py3-none-any.whl
```

## Usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
```

- `width`, `height`: the maze's dimensions in cells.
- `seed`: optional, defaults to `42`. The same seed always produces the
  same maze, so results are reproducible across runs.

The maze is generated immediately, inside `__init__` — there is no
separate "generate" step to call.

### Accessing the generated structure

```python
gen.grid          # list[list[Cell]], indexed gen.grid[x][y]
gen.width          # int
gen.height         # int
gen.pat_42         # True if the "42" pattern was drawn
```

Each `Cell` has:
- `x`, `y`: its position.
- `walls`: a dict `{'N': bool, 'E': bool, 'S': bool, 'W': bool}`,
  `True` meaning that wall is closed.
- `is_blocked`: `True` if the cell is part of the "42" pattern (not a
  walkable maze cell).

If the grid is smaller than 10 in either dimension, the "42" pattern is
skipped (`gen.pat_42` is `False`) and a warning is printed to stderr. The maze itself still generates normally.

### Accessing a solution

```python
path = gen.solve((0, 0), (19, 14))   # start, end as (x, y)
```

Returns the shortest path between any two cells, as a list of `Cell`,
in order from start to end (both included). Uses breadth-first search (bfs),
since the maze is unweighted. `start`/`end` are not fixed at generation
time, you can call `solve()` with whatever two points you need, as many times
as you like, on the same generated maze.

## Quick test

A minimal script to generate a maze, solve it, and write it out in the
subject's output format (IV.5): useful for checking the result with
`maze_analyzer.py`.

```python
from mazegen import MazeGenerator


def hex_conversion(cell) -> str:
    value = 0
    if cell.walls['N']:
        value |= (1 << 0)
    if cell.walls['E']:
        value |= (1 << 1)
    if cell.walls['S']:
        value |= (1 << 2)
    if cell.walls['W']:
        value |= (1 << 3)
    return hex(value)[2:]


def direction_between(cell_a, cell_b) -> str:
    dx = cell_b.x - cell_a.x
    dy = cell_b.y - cell_a.y
    if dy == -1:
        return "N"
    elif dx == 1:
        return "E"
    elif dy == 1:
        return "S"
    elif dx == -1:
        return "W"
    raise ValueError("Error: path cells are not adjacent.")


gen = MazeGenerator(20, 15, seed=42)
path = gen.solve((0, 0), (19, 14))

with open("mazegen_test_output.txt", "w") as f:
    for y in range(gen.height):
        for x in range(gen.width):
            f.write(hex_conversion(gen.grid[x][y]))
        f.write("\n")
    f.write("\n0,0\n19,14\n")
    f.write("".join(
        direction_between(path[i], path[i + 1])
        for i in range(len(path) - 1)
    ) + "\n")
```

## Building from source

```
python3 -m venv .build-venv
.build-venv/bin/pip install build
.build-venv/bin/python3 -m build --wheel
```

Produces `dist/mazegen-1.42-py3-none-any.whl`. (`make package`, run
from the repository root, does the same thing in one step.)

## Scope

This package deliberately includes only what a maze generator needs:
generation and pathfinding. It does not include rendering, terminal
display, colour theming, or any pattern other than "42" as those are
specific to `a_maze_ing.py`'s own use of this package, not the reusable
core. See the main project's `README.md` for the reasoning behind
keeping "42" (and only "42") in this module.