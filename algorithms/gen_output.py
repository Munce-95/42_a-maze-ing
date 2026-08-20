from typing import Tuple, List
from utils_files.cell import Cell


def _hex_conversion(cell: Cell) -> str:
    value: int = 0
    if cell.walls['N']:
        value |= (1 << 0)
    if cell.walls['E']:
        value |= (1 << 1)
    if cell.walls['S']:
        value |= (1 << 2)
    if cell.walls['W']:
        value |= (1 << 3)
    return hex(value)[2:]


def _direction(cell_a: Cell, cell_b: Cell) -> str:
    """
    Determines the compass direction of the step from cell_a to cell_b

    Args:
        cell_a: the starting cell
        cell_b: the adjacent cell stepped into

    Returns:
        One of "N", "E", "S", "W"
    """
    dx = cell_b.x - cell_a.x
    dy = cell_b.y - cell_a.y
    if dy == -1:
        return "N"
    elif dx == 1:
        return "E"
    elif dy == 1:
        return "S"
    elif dx == -1:
        return "W"
    raise ValueError("Error: path cells are not adjacent.")


def write_output_file(output_file: str,
                      entry_coords: Tuple[int, int],
                      exit_coords: Tuple[int, int],
                      maze: List[List[Cell]],
                      path: List[Cell]) -> None:
    width: int = len(maze)
    height: int = len(maze[0])
    with open(output_file, "w") as f:
        for y in range(height):
            for x in range(width):
                hex_digit: str = _hex_conversion(maze[x][y])
                f.write(hex_digit)
            f.write("\n")
        f.write("\n")
        f.write(f"{entry_coords[0]},{entry_coords[1]}\n")
        f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
        path_str = "".join(
            _direction(path[i], path[i + 1])
            for i in range(len(path) - 1)
        )
        f.write(path_str + "\n")
