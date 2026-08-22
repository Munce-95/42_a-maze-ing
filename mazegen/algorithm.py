from .cell import Cell
from typing import List


def remove_wall(cell1: Cell,
                cell2: Cell) -> None:
    """
    This function is used to remove a wall between two cells

    Args:
        cell1: The starting cell
        cell2: The adjacent cell
    """
    dx = cell2.x - cell1.x
    dy = cell2.y - cell1.y
    if dx == 1:
        cell1.walls['E'] = False
        cell2.walls['W'] = False
    elif dx == -1:
        cell1.walls['W'] = False
        cell2.walls['E'] = False
    elif dy == 1:
        cell1.walls['S'] = False
        cell2.walls['N'] = False
    elif dy == -1:
        cell1.walls['N'] = False
        cell2.walls['S'] = False


def get_unblocked_neighbour(grid: List[List[Cell]],
                            cell: Cell,
                            height: int,
                            width: int) -> List[Cell]:
    