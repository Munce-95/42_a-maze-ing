import random


MIN_DISPLAY_SIZE = 10


class Cell:
    def __init__(
            self,
            x: int,
            y: int) -> None:
        self.x = x
        self.y = y
        self.is_blocked = False
        self.walls = {'N': True,
                      'E': True,
                      'S': True,
                      'W': True}


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
        self._apply_pattern()


    def _apply_pattern(self) -> None:
        if self.height < MIN_DISPLAY_SIZE or self.width < MIN_DISPLAY_SIZE:
            self.pat_42 = False
        else:
            self.pat_42 = True