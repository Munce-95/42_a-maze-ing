from typing import NamedTuple, Tuple


class Data(NamedTuple):
    """
    The fully validated, immutable configuration produced by parsing.py,
    handed off to the maze generator and TUI as the single source of
    truth for a session

    Parameters
    ----------
    width : int
        maze width in cells
    height : int
        maze height in cells
    entry : Tuple[int, int]
        entry coordinates (x, y)
    exit_ : Tuple[int, int]
        exit coordinates (x, y)
    output_file : str
        name of the file the generated maze will be written to
    perfect : bool
        True for a perfect maze (single path), False for a
        playable board with loops
    seed : int
        Seed for the random number generator, used once at program
        start so the first generated maze is reproducible across runs
        with the same value.
    pattern : str
        name of the selected pattern (defaults to "PATTERN_42")
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit_: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: int
    pattern: str
