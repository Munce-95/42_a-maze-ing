from typing import List, Tuple

MazeGenerator(width, height, seed)


class Cell:
    def __init__(
            self,
            x: int,
            y: int) -> None:
        self.x = x
        self.y = y
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