import random
import sys
from .cell import Cell
from typing import List, Tuple
from .algorithm import generate_wilson, non_perfect, bfs


MIN_DISPLAY_SIZE = 10

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0]
]


class MazeGenerator:
    """
    Generates a Pac-Man-style maze: fully connected, always contains
    at least two independent loops (never a single-path/"perfect"
    maze), and includes a visible "42" pattern when the grid is
    large enough.

    Examples
    --------
    >>> gen = MazeGenerator(width=20, height=15, seed=42)
    >>> gen.grid            # list[list[Cell]], gen.grid[x][y]
    >>> gen.pat_42           # True if the 42 pattern was drawn
    >>> gen.solve((0, 0), (19, 14))  # shortest path as a list of Cell

    Parameters
    ----------
    width : int
        maze width in cells.
    height : int
        maze height in cells.
    seed : int
        seed for reproducible generation (default 42).
    """
    def __init__(
            self,
            width: int,
            height: int,
            seed: int = 42) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self._rng = random.Random(seed)
        self.pat_42 = False
        self.grid = [[Cell(x, y) for y in range(height)]
                     for x in range(width)]
        self._apply_pattern()
        generate_wilson(self.grid, self.width, self.height, self._rng)
        non_perfect(self.grid, self.width, self.height)

    def _apply_pattern(self) -> None:
        """
        Draws the "42" pattern centered in the grid, marking the
        relevant cells is_blocked. Skips drawing (setting pat_42 to
        False and printing a warning) if the grid is smaller than
        MIN_DISPLAY_SIZE in either dimension.
        """
        if self.height < MIN_DISPLAY_SIZE or self.width < MIN_DISPLAY_SIZE:
            self.pat_42 = False
            print("Warning: the grid is too small to display the pattern",
                  file=sys.stderr)
        else:
            self.pat_42 = True
            pat_h, pat_w = len(PATTERN_42), len(PATTERN_42[0])
            start_x = (self.width - pat_w) // 2
            start_y = (self.height - pat_h) // 2
            for py in range(pat_h):
                for px in range(pat_w):
                    val = PATTERN_42[py][px]
                    target = self.grid[start_x + px][start_y + py]
                    if val:
                        target.is_blocked = True

    def solve(self,
              start: Tuple[int, int],
              end: Tuple[int, int]) -> List[Cell]:
        """
        Finds the shortest path between two cells in this maze.

        Parameters
        ----------
        start : Tuple[int, int]
            starting coordinates (x, y), e.g. the player's
            spawn point.
        end : Tuple[int, int]
            target coordinates (x, y), e.g. a ghost's spawn
            point.

        Returns
        -------
        List[Cell]
            The shortest path from start to end, as a list of Cell,
            in order (inclusive of both endpoints).
        """
        return bfs(self.grid, self.width, self.height, start, end)
