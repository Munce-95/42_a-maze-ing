# A-Maze-ing — Evaluation Walkthrough

## 1. The config file

Open `config.txt`. Point out the mandatory keys:

- `WIDTH`, `HEIGHT` — grid size (3–50)
- `ENTRY`, `EXIT` — `x,y` coordinates
- `OUTPUT_FILE` — must end in `.txt`
- `PERFECT` — `True`/`False`

Then the optional keys added on top of the subject: `SEED` (reproducibility),
and the `PATTERN_*` toggles (`PATTERN_PENGUIN`, `PATTERN_HEART`, `PATTERN_CEL`,
`PATTERN_MATT`, `PATTERN_SANS`).

Mention briefly, without necessarily demoing each: comments (`#`), blank
lines, indentation rules, and duplicate-key handling are all validated.

## 2. Run it

```
python3 a_maze_ing.py config.txt
```

Walk through what happens, in order:

1. `check_args` — confirms the file exists, is a file, and is named
   `config.txt` (a deliberate choice, enforced beyond what the subject
   requires).
2. `retrieve_raw_data` — reads and parses the file into a dict, skipping
   comments/blanks, rejecting malformed lines.
3. `check_raw_data` — confirms the six mandatory keys are present and
   well-formed.
4. `check_values` — runs each validator in turn: dimensions, `PERFECT`,
   output filename, entry/exit format/bounds/equality, pattern selection,
   pattern-exclusion, seed. Each raises a clear, specific error on failure.
5. `get_parsed_values` — packages everything into `Data`, an immutable
   `NamedTuple` and the single handoff point between parsing and
   generation.

## 3. The rendered maze

The maze renders in colour immediately. Talking points:

- **Wilson's algorithm** builds a perfect maze first (a spanning tree — no
  loops).
- Since `PERFECT=False` by default, a **second pass removes dead-ends**
  (cells with exactly one open wall) until none remain, producing a
  Pac-Man-style board with multiple independent routes.
- The **"42" pattern** is visible, drawn from cells marked closed/blocked.

## 4. The interactive menu

- `1` — regenerate (new maze, same session; show it's genuinely different
  from the last one).
- `2` — toggle the shortest-path overlay on/off.
- `3` — cycle wall colours.
- `q` — quit cleanly.
- Ctrl+C / Ctrl+D — also handled gracefully, no traceback.

## 5. The output file

```
cat output_file.txt
```

- Hex-encoded walls, one row per line.
- Blank line.
- Entry coordinates, exit coordinates, shortest path as N/E/S/W letters.

This is the format `maze_analyzer.py` checks for wall-coherence and
perfect/playable validity.

## 6. Reproducibility — demonstrate live

Run the program twice with the same `SEED`, diff the outputs:

```
python3 a_maze_ing.py config.txt   # quit immediately
cp output_file.txt run1.txt
python3 a_maze_ing.py config.txt   # quit immediately
diff run1.txt output_file.txt      # → no output = identical
```

Then, within a **single** run, press `1` (regenerate) and show the maze
changes — the random sequence keeps advancing rather than resetting, so
only the *first* maze per seed is reproducible, not every regeneration.

## 7. `mazegen` — the reusable package

Separately from the live project, the generation logic is packaged as a
standalone, pip-installable module.

```
make package          # builds dist/mazegen-*.whl in an isolated venv
```

Ideally in a fresh terminal or venv, to make the self-containment concrete:

```
pip install dist/mazegen-1.42-py3-none-any.whl
python3 -c "
from mazegen import MazeGenerator
gen = MazeGenerator(20, 15, seed=42)
print(gen.solve((0, 0), (19, 14)))
"
```

Talking points:

- No dependency on the rest of the repo — works completely standalone.
- Includes the mandatory "42" pattern (confirmed with staff that this
  applies to the reusable module too).
- Excludes theming and the other optional patterns — a future project
  reusing this wouldn't want this project's specific extras baked in.

## 8. Tooling, if asked

```
make lint      # flake8 + mypy, both clean
make debug     # drops into pdb at program start
```

## Appendix — key functions, if asked to explain the code

### `generate_wilson` (`algorithms/wilson.py`, and adapted in `mazegen/algorithm.py`)

Implements **Wilson's algorithm**: loop-erased random walk.

- Start with one arbitrary cell "in the maze," everything else
  "unvisited."
- Repeatedly pick a random unvisited cell and walk randomly from it,
  one step at a time, until the walk reaches a cell already in the
  maze.
- If the walk crosses its own path (a loop), that loop is erased —
  the path is cut back to the earlier visit — before continuing.
- Once the walk reaches the maze, the (loop-erased) path it took is
  carved in: walls are opened between each consecutive pair of cells,
  and those cells join the maze.
- Repeats until every cell has joined.

Why it matters: this produces a **perfect maze** (spanning tree, no
cycles) with a mathematically uniform distribution over all possible
mazes for the grid — no bias toward long corridors or short ones,
unlike some simpler algorithms (e.g. plain randomized DFS).

### `non_perfect` (`algorithms/wilson.py`, and `mazegen/algorithm.py`)

Runs after `generate_wilson`, only when `PERFECT=False`.

- Scans the grid for **dead-ends**: cells with exactly one open wall
  (three closed walls).
- For each one, breaks a wall toward a valid neighbor — since every
  cell is already connected via the spanning tree, breaking any wall
  between two cells creates exactly one loop.
- Repeats the full scan until no dead-ends remain (breaking a wall
  can only reduce the dead-end count, never increase it, so this is
  guaranteed to terminate).
- Ignores pattern cells (`is_blocked`/etc.) entirely — those aren't
  real maze cells.

Result: full connectivity (already guaranteed), multiple independent
loops, and — deliberately — zero dead-ends beyond the "42" pattern
itself, going past the subject's baseline ("dead-ends should stay
rare") toward the bonus ("no dead-end at all").

### `bfs` (`mazegen/algorithm.py`) / `solve_dijkstra` (`algorithms/dijkstra.py`)

Finds the shortest path between two cells in an **already-generated**
maze.

- Since every move between connected cells costs the same (the maze
  is unweighted), **breadth-first search** is used in `mazegen` — the
  simpler, correct tool for this case, rather than a weighted
  algorithm like Dijkstra.
- Explores outward from the start cell, one "ring" of distance at a
  time, tracking for each newly-discovered cell which cell led to it
  (`came_from`).
- Stops the moment the target cell is reached, then walks backward
  through `came_from` to reconstruct the path, and reverses it to
  read start → end.
- Only considers **walkable** neighbors — cells connected by an
  actually-open wall — unlike the neighbor-finding used during
  generation, which only cares about pattern-blocking, not wall
  state.

### `Data` (`utils_files/data.py`, and `mazegen`'s constructor arguments)

An immutable `NamedTuple` holding the fully validated configuration.
Acts as the single, deliberate handoff point between the parsing
module and everything downstream (generation, rendering, output
writing) — nothing past `parsing.py` ever touches the raw config
dict directly.

### `MazeGenerator` (`mazegen/generator.py`)

The reusable package's public class. Generates the maze immediately
on construction (`__init__` builds the grid, places the "42" pattern
if the grid is large enough, runs Wilson's algorithm, then the
dead-end-removal pass — always, since `mazegen` has no `PERFECT`
option, a Pac-Man-style maze never needs a single-path mode).
Exposes the structure directly (`gen.grid`) and a solution on demand
(`gen.solve(start, end)`, not fixed at generation time, so a future
project can pick its own start/end points at runtime).
