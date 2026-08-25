*This project has been created as part of the 42 curriculum by celgremy & mgedeon.*

# Description

A-Maze-ing is a Python maze generator built for the 42 curriculum. It reads a
configuration file, generates a maze (either a perfect maze with exactly one
path between entry and exit, or a Pac-Man-style playable board with loops)
and writes it to a file using a hexadecimal wall representation. The maze
always contains a visible "42" pattern (unless the grid is too small to fit
it), and can optionally display alternative patterns instead, selected
through the configuration file. The project also provides a terminal (TUI)
visual representation of the generated maze, and organizes the maze
generation logic as a reusable, pip-installable module (`mazegen`).

# Instructions

Run the program with:

```
python3 a_maze_ing.py config.txt
```

- `a_maze_ing.py` is the main program entry point.
- `config.txt` is the required configuration file name (see below for its
  format).

The project ships with a `Makefile` exposing the following targets:

- `make install`: install project dependencies (none, outside the Python
  standard library).
- `make run`: run the main script against `config.txt`.
- `make debug`: run the main script under `pdb`.
- `make clean`: remove temporary files, caches, and build artifacts.
- `make lint`: run `flake8` and `mypy` with the required flags.
- `make lint-strict`: run `flake8` and `mypy --strict` (optional, stricter).
- `make package`: build the `mazegen` package from source, in an isolated
  virtual environment, producing `dist/mazegen-*.whl`.

The program validates the configuration file and reports any error (missing
file, bad syntax, invalid or out-of-range values, permission issues, etc.)
with a clear message instead of crashing.

# Resources
- [numpydoc Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html) — docstring format conventions used throughout the project.
- [Maze Generation Algorithms – An Exploration](https://professor-l.github.io/mazes/) — animated explanations of perfect-maze algorithms, including Wilson's.
- [Wilson's Algorithm (visualization)](https://gist.github.com/mbostock/11357811) — visual demo of loop-erased random walks producing a uniform spanning tree.
- [Generating Mazes](https://healeycodes.com/generating-mazes) — comparison of maze algorithms and their bias trade-offs.
- [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) — official Python Packaging User Guide, used to build `mazegen`'s wheel.
- [pdb — The Python Debugger](https://docs.python.org/3/library/pdb.html) — official docs for the debugger used by `make debug`.
- [BFS video](https://www.youtube.com/watch?v=HZ5YTanv5QE): Used to understand BFS algo.
- [Docstring documentation](https://www.geeksforgeeks.org/python/python-docstrings/): Used to understand Docstring and the difference between Google and Numpydoc styles.
- [A-Maze-ing Visualizer](https://amazeing.app/simulation/): Used to visualize and verify the execution of both Wilson's and Dijkstra's algorithms.

**AI usage**:

Claude was used as a peer-review / rubber-duck assistant
throughout the parsing module (`parsing.py`, `utils_files/`) and the
`mazegen` package, under strict rules: no code was written by the AI
directly, and no code blocks were provided.
Claude's role was to ask questions, point out bugs and edge cases, and flag style and
PEP 8/NumPy-docstring concerns without supplying the fix. All code was written and tested by the author.

Gemini was used to help explain certain concepts, such as tracking visited cells and pattern generation across the maze. It also assisted with refactoring long functions in `wilson.py`. 
The AI was primarily used as help to translate conceptual ideas into code.
Every prompt explicitly instructed the model not to write code directly, limiting output to explanations or pseudocode.
As a result, 95% of the code was written by hand.

## Config file's structure

The configuration file (`config.txt`, name enforced) contains one
`KEY=VALUE` pair per line.

- Lines starting with `#` are treated as comments and ignored, regardless of
  what follows on that line.
- Lines starting with a space are rejected with an error — including a
  comment line indented with a leading space (deliberate choice: indentation
  before `#` is not supported).
- Blank lines are ignored.
- Keys are case-insensitive and are normalized to uppercase internally.
- A key may only contain letters and underscores.
- A line must contain exactly one `=`; a line with none, or more than one,
  is rejected.
- If the same key appears more than once, the **first** occurrence is kept
  and later duplicates are ignored.

Mandatory keys:

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width, integer, `3`–`50` | `WIDTH=20` |
| `HEIGHT` | Maze height, integer, `3`–`50` | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `x,y`, inside the grid | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `x,y`, inside the grid, different from `ENTRY` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename, must end in `.txt` | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` or `False` (case-insensitive) | `PERFECT=True` |

`ENTRY` and `EXIT` must both lie inside the grid bounds, must not be equal
to each other, and must not fall inside the "42" pattern's footprint
unless the grid is smaller than 10×10 in either dimension, in which case the
pattern is not displayed at all, a warning is printed to `stderr`, and this
last restriction is skipped.

Optional keys: pattern selection (not required by the subject, documented
here as an added feature): `PATTERN_PENGUIN`, `PATTERN_HEART`,
`PATTERN_CEL`, `PATTERN_MATT`, `PATTERN_SANS`, each accepting `True`/`False`.
At most one should be set to `True`. If none, or more than one, is set to
`True`, the maze silently falls back to displaying the default "42"
pattern.

Optional key: reproducibility: `SEED`, an integer. Defaults to `42` if
omitted. Seeds Python's random module once, at program start, so the first
maze generated for a given seed is always identical across runs.
Regenerating (option 1 in the terminal menu) still produces a different
maze each time within the same run, since the random sequence keeps
advancing rather than resetting.

## Maze generation algorithm

Mazes are generated with **Wilson's algorithm** (loop-erased random walk):
starting from an arbitrary cell, the algorithm repeatedly performs a random
walk from an unvisited cell until it reaches the growing maze, erasing any
loop the walk creates along the way, then carves that loop-erased path into
the maze. This produces a perfect maze (a spanning tree with exactly one
path between any two cells) with a uniform distribution over all possible
mazes for the given grid.

When `PERFECT=False` (the default), a second pass removes dead-ends: the
grid is repeatedly scanned for cells with exactly one open wall (three
closed walls), and one wall is broken toward a valid neighbor, until no
dead-ends remain among real (non-pattern) cells. This produces the
Pac-Man-style playable board required by the subject: full connectivity,
multiple independent loops, and no dead-ends beyond what the "42" pattern
itself creates.

## Why did we choose this algorithm

We originally planned to use the Kruskal's algorithm for the maze generation. After discussing with some peers about their **A-Maze-Ing** project, we decided to work with Wilson's algorithm, because it is easier to implement than Kruskal.
And for the pathfinding, we wanted to avoid what others usually use, and opted for Dijkstra's algorithm.

## What part of the code is reusable? How?

The maze generation logic is packaged as `mazegen`, a standalone,
pip-installable Python package (`mazegen-1.42-py3-none-any.whl`, built via
`make package`). It exposes a single class, `MazeGenerator`, that:

- Takes `width`, `height`, and an optional `seed` at construction, and
  generates the maze immediately (Wilson's algorithm, followed by the same
  dead-end-removal pass described above = `mazegen`'s mazes are always
  loopy, since a Pac-Man-style consumer never needs a single-path maze).
- Exposes the generated structure directly as `gen.grid`
  (`list[list[Cell]]`), where each `Cell` holds its position, its four
  wall states, and whether it belongs to the "42" pattern.
- Exposes a solution on demand via `gen.solve(start, end)`, returning the
  shortest path (breadth-first search) between any two coordinates. It's called
  whenever needed, not fixed at generation time, so a consuming project can
  pick its own start/end points (e.g. player and ghost spawn points) at
  runtime.

`mazegen` has zero third-party dependencies and does not depend on any
other file in this repository = it is fully self-contained inside the
`mazegen/` package, and the built wheel installs and runs standalone. Full
usage documentation lives in `mazegen/README.md` and in `MazeGenerator`'s
own docstring.

### On the "42" pattern in `mazegen`

The subject's mandatory maze requirements (Chapter IV) call for a visible
"42" pattern drawn by closed cells. After confirming with other people that this
applies to the reusable module as well, `mazegen`'s `MazeGenerator` does
include the "42" pattern (and only "42", no other alternate pattern, and
no theming), drawn under the same rules as the live project (skipped, with
a warning, if the grid is smaller than 10×10). The other optional patterns
(`PATTERN_PENGUIN`, `PATTERN_HEART`, etc.) and all colour theming remain
specific to `a_maze_ing.py`'s own terminal display and are not part of the
reusable package, since a future project reusing `mazegen` would have no
reason to want this project's specific extra patterns or colours.

## Team and project management

### Roles of each team member

- **celgremy** — the live project's visual representation (terminal
  rendering, colours) and the maze generation algorithm (Wilson's
  algorithm, dead-end removal for the loopy mode).
- **mgedeon** — configuration parsing and validation (`parsing.py`,
  `utils_files/`), and adapting the generation logic into the
  standalone `mazegen` package.


### Anticipated planning and how it evolved

Config parsing and the maze generation algorithm were built in parallel
from the start, meeting at a small set of agreed interfaces (the `Data`
object, and later a shared understanding of `Cell`'s wall representation).

Several pieces were reworked as requirements became clearer along the
way: the pattern system grew from just the mandatory "42" into several
optional selectable patterns, the `PERFECT=False` mode moved from a
random wall-removal ratio to a dead-end-targeted approach once the
ratio-based version failed the analyzer, and the reusable `mazegen`
package's scope changed more than once (single-file vs. proper
sub-package, and whether it should include the "42" pattern at all,
settled after checking directly with other people).

The interactive terminal
menu, seed reproducibility, and full documentation/packaging pass were
added later, once the core generation and parsing were stable.

### What worked well and what could be improved

This isn't our first project working together, so we already knew each
other's strengths going in, which let us split the work quickly and
work mostly in parallel rather than figuring that out along the way.
What could be improved: time management.

### Did we use any specific tools? Which ones?

GitHub (version control, collaboration) and Discord (communication).