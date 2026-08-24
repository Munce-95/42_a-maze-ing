from typing import NamedTuple, Optional


class Data(NamedTuple):
    """
    The fully validated, immutable configuration produced by parsing.py,
    handed off to the maze generator and TUI as the single source of
    truth for a session

    Args:
        width: maze width in cells
        height: maze height in cells
        entry: entry coordinates (x, y)
        exit_: exit coordinates (x, y)
        output_file: name of the file the generated maze will be written to
        perfect: True for a perfect maze (single path), False for a
            playable board with loops
        pattern: name of the selected pattern (defaults to "PATTERN_42")
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int
    pattern: str
