*This project has been created as part of the 42 curriculum by celgremy & mgedeon.*

# Description

A-Maze-ing is a Python maze generator built for the 42 curriculum. It reads a
configuration file, generates a maze — either a perfect maze (exactly one
path between entry and exit) or a Pac-Man-style playable board with loops —
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

- `make install` — install project dependencies (none, outside the Python
  standard library).
- `make run` — run the main script against `config.txt`.
- `make debug` — run the main script under `pdb`.
- `make clean` — remove temporary files, caches, and build artifacts.
- `make lint` — run `flake8` and `mypy` with the required flags.
- `make lint-strict` — run `flake8` and `mypy --strict` (optional, stricter).
- `make package` — build the `mazegen` package from source, in an isolated
  virtual environment, producing `dist/mazegen-*.whl`.

The program validates the configuration file and reports any error (missing
file, bad syntax, invalid or out-of-range values, permission issues, etc.)
with a clear message instead of crashing.

# Resources

TODO: list documentation, articles, and tutorials consulted for maze
generation algorithms (Wilson's algorithm, dead-end removal for loopy
mazes) and Python packaging.

**AI usage**: Claude was used as a peer-review / rubber-duck assistant
throughout the parsing module (`parsing.py`, `utils_files/`) and the
`mazegen` package, under strict rules: no code was written by the AI
directly, and no code blocks were provided unless explicitly requested.
Claude's role was to ask questions, point out bugs and edge cases (e.g.
duplicate/indented/commented config lines, off-by-one bounds errors,
exception-type mismatches, `NamedTuple` misuse, `dict`/module import
issues, Wilson's algorithm and BFS traced by hand), and flag style and
PEP 8/NumPy-docstring concerns — without supplying the fix unless directly
asked, and clearly flagged when it was. All code was written, tested, and
understood by the author before being kept.

TODO: add a note here on any AI usage in the maze generation algorithm
(`wilson.py`) or TUI display, if applicable to that teammate's work.

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
to each other, and must not fall inside the "42" pattern's footprint —
unless the grid is smaller than 10×10 in either dimension, in which case the
pattern is not displayed at all, a warning is printed to `stderr`, and this
last restriction is skipped.

Optional keys — pattern selection (not required by the subject, documented
here as an added feature): `PATTERN_PENGUIN`, `PATTERN_HEART`,
`PATTERN_CEL`, `PATTERN_MATT`, `PATTERN_SANS`, each accepting `True`/`False`.
At most one should be set to `True`. If none, or more than one, is set to
`True`, the maze silently falls back to displaying the default "42"
pattern.

Optional key — reproducibility: `SEED`, an integer. Defaults to `42` if
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
the maze. This produces a perfect maze — a spanning tree with exactly one
path between any two cells — with a uniform distribution over all possible
mazes for the given grid.

When `PERFECT=False` (the default), a second pass removes dead-ends: the
grid is repeatedly scanned for cells with exactly one open wall (three
closed walls), and one wall is broken toward a valid neighbor, until no
dead-ends remain among real (non-pattern) cells. This produces the
Pac-Man-style playable board required by the subject: full connectivity,
multiple independent loops, and no dead-ends beyond what the "42" pattern
itself creates.

## Why did we choose this algorithm

TODO (owned by the teammate who implemented generation) — briefly, why
Wilson's algorithm was chosen over alternatives like Prim's or Kruskal's
(e.g. unbiased maze distribution, simplicity of implementation).

## What part of the code is reusable? How?

The maze generation logic is packaged as `mazegen`, a standalone,
pip-installable Python package (`mazegen-1.42-py3-none-any.whl`, built via
`make package`). It exposes a single class, `MazeGenerator`, that:

- Takes `width`, `height`, and an optional `seed` at construction, and
  generates the maze immediately (Wilson's algorithm, followed by the same
  dead-end-removal pass described above — `mazegen`'s mazes are always
  loopy, since a Pac-Man-style consumer never needs a single-path maze).
- Exposes the generated structure directly as `gen.grid`
  (`list[list[Cell]]`), where each `Cell` holds its position, its four
  wall states, and whether it belongs to the "42" pattern.
- Exposes a solution on demand via `gen.solve(start, end)`, returning the
  shortest path (breadth-first search) between any two coordinates — called
  whenever needed, not fixed at generation time, so a consuming project can
  pick its own start/end points (e.g. player and ghost spawn points) at
  runtime.

`mazegen` has zero third-party dependencies and does not depend on any
other file in this repository — it is fully self-contained inside the
`mazegen/` package, and the built wheel installs and runs standalone. Full
usage documentation lives in `mazegen/README.md` and in `MazeGenerator`'s
own docstring.

### On the "42" pattern in `mazegen`

The subject's mandatory maze requirements (Chapter IV) call for a visible
"42" pattern drawn by closed cells. After confirming with staff that this
applies to the reusable module as well, `mazegen`'s `MazeGenerator` does
include the "42" pattern (and only "42" — no other alternate pattern, and
no theming), drawn under the same rules as the live project (skipped, with
a warning, if the grid is smaller than 10×10). The other optional patterns
(`PATTERN_PENGUIN`, `PATTERN_HEART`, etc.) and all colour theming remain
specific to `a_maze_ing.py`'s own terminal display and are not part of the
reusable package, since a future project reusing `mazegen` would have no
reason to want this project's specific extra patterns or colours.

## Team and project management

### Roles of each team member

TODO.

### Anticipated planning and how it evolved

TODO.

### What worked well and what could be improved

TODO.

### Did we use any specific tools? Which ones?

TODO.