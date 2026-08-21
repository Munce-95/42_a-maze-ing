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
generation logic as a reusable, pip-installable module.

# Instructions

Run the program with:

```
python3 a_maze_ing.py config.txt
```

- `a_maze_ing.py` is the main program entry point.
- `config.txt` is the configuration file (see below for its format). A
  different filename can be passed as the sole argument.

The project ships with a `Makefile` exposing the following targets:

- `make install` — install project dependencies.
- `make run` — run the main script.
- `make debug` — run the main script in debug mode (`pdb`).
- `make clean` — remove temporary files/caches (`__pycache__`, `.mypy_cache`).
- `make lint` — run `flake8` and `mypy` with the required flags.
- `make lint-strict` — run `flake8` and `mypy --strict` (optional, stricter).

The program validates the configuration file and reports any error (missing
file, bad syntax, invalid or out-of-range values, etc.) with a clear message
instead of crashing.

# Resources

TODO: list documentation, articles, and tutorials consulted for maze
generation algorithms and Python packaging (this section belongs to whoever
worked on the generation algorithm and the reusable module).

**AI usage**: Claude was used as a peer-review / rubber-duck assistant
throughout the parsing module (`parsing.py`, `utils_files/`), under strict
rules: no code was written by the AI directly, and no code blocks were
provided unless explicitly requested. Claude's role was to ask questions,
point out bugs and edge cases (e.g. duplicate/indented/commented config
lines, off-by-one bounds errors, exception-type mismatches, `NamedTuple`
misuse, `dict`/module import issues), and flag style and PEP 8 concerns —
without supplying the fix. All code in the parsing module was written,
tested, and understood by the author.

TODO: add a note here on any AI usage in the maze generation algorithm or
TUI display, if applicable.

## Config file's structure

The configuration file (`config.txt` by default) contains one `KEY=VALUE`
pair per line.

- Lines starting with `#` are treated as comments and ignored, regardless of
  what follows on that line.
- Lines starting with a space are rejected with an error — including a
  comment line indented with a leading space (deliberate choice: indentation
  before `#` is not supported).
- Blank lines are ignored.
- Keys are case-insensitive and are normalized to uppercase internally.
- A key may only contain letters and underscores.
- If the same key appears more than once, the **first** occurrence is kept
  and later duplicates are ignored.
- A line may contain at most one `=` character; anything after the first
  `=` is taken as the value verbatim (a second `=` in the value is
  rejected).

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

TODO: document any additional keys used by the generation algorithm (e.g.
`SEED`), once finalized.

## Maze generation algorithm

TODO (owned by the teammate handling generation): name the algorithm used
(e.g. recursive backtracker, Prim's, Kruskal's) and describe how it builds
the maze for both the `PERFECT=True` and `PERFECT=False` modes.

## Why did we choose this algorithm

TODO (owned by the teammate handling generation).

## What part of the code is reusable? How?

TODO: describe the `MazeGenerator` reusable module (Chapter VI of the
subject) once built and packaged — how to instantiate it, pass parameters,
and access the generated structure/solution.

The configuration-parsing module (`parsing.py`, `utils_files/`) produces a
single immutable `Data` object (a `typing.NamedTuple`) holding the fully
validated configuration (`width`, `height`, `entry`, `exit_`, `output_file`,
`perfect`, `pattern`), which is handed off to the maze generator as its
input — decoupling config parsing from generation.

## Team and project management

### Roles of each team member

TODO.

### Anticipated planning and how it evolved

On the "42" pattern in mazegen

The subject's mandatory maze requirements (Chapter IV) call for a visible "42" pattern drawn by closed cells. However, the reusable MazeGenerator module (Chapter VI) is deliberately built without this pattern. The subject frames Chapter VI's reusability requirement around a maze generator that later projects can build on — and a hardcoded "42" logo has no reason to appear in an unrelated project reusing this module. We treat the "42" pattern as specific to a_maze_ing.py's own output, not as a property the generic, reusable generator itself needs to guarantee. MazeGenerator produces a plain, loopy (Pac-Man-style) maze with no pattern baked in.

### What worked well and what could be improved

TODO.

### Did we use any specific tools? Which ones?

TODO.