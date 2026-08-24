class Cell:
    """
    A single cell in the maze grid.

    Tracks its position, its four cardinal walls (all closed by
    default, opened as the maze is carved), and whether it is
    reserved by the "42" pattern (is_blocked) rather than being a
    real, walkable maze cell.

    Parameters
    ----------
    x : int
        the cell's column index
    y : int
        the cell's row index
    """
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
