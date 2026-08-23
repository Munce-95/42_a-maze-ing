import random
from typing import List
from .cell import Cell
from .algorithm import generate_wilson, non_perfect


MIN_DISPLAY_SIZE = 10

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0]
]


class MazeGenerator:
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
