class Cell:
    def __init__(
            self,
            x: int,
            y: int) -> None:
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.is_blocked = False
        self.in_symbol = False
        self.sans_eye = False
