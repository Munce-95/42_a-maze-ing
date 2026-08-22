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
