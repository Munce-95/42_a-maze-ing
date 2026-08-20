class Cell:
    """
    A single cell in the maze grid

    Tracks its position, its four cardinal walls (all closed by
    default, opened as the maze is carved), and whether it is
    reserved by the displayed pattern (blocked, part of the symbol,
    or a SANS "eye" cell) rather than being a real, walkable
    maze cell

    Args:
        x: the cell's column index
        y: the cell's row index
    """
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
