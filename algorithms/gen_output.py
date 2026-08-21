from typing import Tuple, List, NamedTuple
from utils_files.cell import Cell


def _hex_conversion(cell: Cell) -> str:
	"""
    Encodes a cell's four walls as a single hexadecimal digit

    Each wall contributes one bit if closed (0=open): North is bit 0,
    East is bit 1, South is bit 2, West is bit 3, per the output
    file's wall-encoding format

    Args:
        cell: the cell whose walls are being encoded

    Returns:
        A single hex character ("0"-"f") representing the closed walls
    """
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


def write_output_file(parsed: NamedTuple,
                      maze: List[List[Cell]],
                      path: List[Cell]) -> None:
    """
    Creates and writes inside the output_file:
    the matrix translated into hexadecimal,
    entry and exit coordinates, the path towards the exit.

    Args:
        parsed: All the parsed data from the config.txt file
        maze: matrix used to be translates into hexa
        path: path from ENTRY to EXIT
    """
	width: int = len(maze)
    height: int = len(maze[0])
    with open(parsed.output_file, "w") as f:
        for y in range(height):
            for x in range(width):
                hex_digit: str = _hex_conversion(maze[x][y])
                f.write(hex_digit)
            f.write("\n")
        f.write("\n")
        f.write(f"{parsed.entry[0]},{parsed.entry[1]}\n")
        f.write(f"{parsed.exit_[0]},{parsed.exit_[1]}\n")
        path_str = "".join(
            _direction(path[i], path[i + 1])
            for i in range(len(path) - 1)
        )
        f.write(path_str + "\n")
