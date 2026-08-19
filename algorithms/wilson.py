import random
import sys
import subprocess
from errors import exit_program
from typing import List, Tuple, Dict, NamedTuple
from utils_files.pattern import PATTERN_SANS, get_pattern_by_name
from utils_files.themes import get_bg_list_for_pattern
from algorithms.dijkstra import solve_dijkstra, mark_path_in_matrix
from utils_files.cell import Cell


current_bg_list: List[str] = []


def is_obstacle(cell: Cell) -> bool:
    """Check if the cell is part of the symbol or a wall"""
    return cell.is_blocked or cell.in_symbol or cell.sans_eye


def remove_wall(
        cell1: Cell,
        cell2: Cell) -> None:
    """This function is used to remove a wall between two cells"""
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


def non_perfect(
        grid: List[List[Cell]],
        width: int,
        height: int,
        ratio: float = 0.15) -> None:
    """This function break random wall in the maze already generated
    to make it 'non-perfect'"""
    remove_walls: List[Tuple[Cell, Cell]] = []
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            if is_obstacle(cell):
                continue
            if cell.walls['E'] and x + 1 < width:
                neighbor = grid[x + 1][y]
                if not is_obstacle(neighbor):
                    remove_walls.append((cell, neighbor))
            if cell.walls['S'] and y + 1 < height:
                neighbor = grid[x][y + 1]
                if not is_obstacle(neighbor):
                    remove_walls.append((cell, neighbor))
    num_to_remove = int(len(remove_walls) * ratio)
    walls_to_remove = random.sample(
        remove_walls,
        min(num_to_remove, len(remove_walls))
    )
    for cell1, cell2 in walls_to_remove:
        remove_wall(cell1, cell2)


def apply_pattern(
        grid: List[List[Cell]],
        width: int,
        height: int,
        pattern: str) -> bool:
    """This function will pregenerate the pattern within the maze's edge"""
    pattern_matrix = get_pattern_by_name(pattern)
    is_sans = (pattern_matrix == PATTERN_SANS)
    bg_list = get_bg_list_for_pattern(is_sans)
    if width < 10 or height < 10:
        return is_sans, bg_list
    pat_h, pat_w = len(pattern_matrix), len(pattern_matrix[0])
    start_x = (width - pat_w) // 2
    start_y = (height - pat_h) // 2
    for py in range(pat_h):
        for px in range(pat_w):
            val = pattern_matrix[py][px]
            target = grid[start_x + px][start_y + py]
            if val == 1:
                target.is_blocked = True
            elif val == 2:
                target.in_symbol = True
            elif val == 3:
                target.sans_eye = True
    return is_sans, bg_list


def get_unblocked_neighbors(
        grid: List[List[Cell]],
        cell: Cell,
        width: int,
        height: int) -> List[Cell]:
    """Return the cells that are not obstacles"""
    neighbors = []
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = cell.x + dx, cell.y + dy
        if (
                0 <= nx < width
                and 0 <= ny < height
                and not is_obstacle(grid[nx][ny])):
            neighbors.append(grid[nx][ny])
    return neighbors


def generate_wilson(
        width: int,
        height: int,
        pattern: str,
        parsed: NamedTuple) -> List[List[Cell]]:
    """This function is the main part of the maze.
    It generate the whole maze using the Wilson's Algorithm"""
    grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
    is_sans, bg_list = apply_pattern(grid, width, height, pattern)
    unvisited = [
        grid[x][y] for x in range(width)
        for y in range(height)
        if not is_obstacle(grid[x][y])]
    if not unvisited:
        return grid, is_sans, bg_list
    first_cell = random.choice(unvisited)
    unvisited.remove(first_cell)
    while unvisited:
        current = random.choice(unvisited)
        path = [current]
        while current in unvisited:
            neighbors = get_unblocked_neighbors(grid, current, width, height)
            current = random.choice(neighbors)
            if current in path:
                path = path[:path.index(current) + 1]
            else:
                path.append(current)
        for i in range(len(path) - 1):
            remove_wall(path[i], path[i + 1])
            if path[i] in unvisited:
                unvisited.remove(path[i])
    if not parsed.perfect:
        non_perfect(grid, width, height)
    return grid, is_sans, bg_list


def build_matrix_1x1(
        grid: List[List[Cell]],
        width: int,
        height: int,
        is_sans: bool = False) -> Tuple[List[List[str]], int, int]:
    """This function build the maze with characters"""
    render_w = width * 2 + 1
    render_h = height * 2 + 1
    output_grid = [["W" for _ in range(render_w)] for _ in range(render_h)]
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            rx, ry = x * 2 + 1, y * 2 + 1

            if cell.is_blocked:
                output_grid[ry][rx] = "B"
            elif cell.in_symbol:
                output_grid[ry][rx] = "C"
            elif cell.sans_eye:
                output_grid[ry][rx] = "I"
            else:
                output_grid[ry][rx] = " "
                if not cell.walls['E']:
                    output_grid[ry][rx + 1] = " "
                if not cell.walls['S']:
                    output_grid[ry + 1][rx] = " "
    if is_sans:
        _merge_sans_blocks(grid, output_grid, width, height)
    return output_grid, render_w, render_h


def _merge_sans_blocks(
        grid: List[List[Cell]],
        output_grid: List[List[str]],
        width: int,
        height: int) -> None:
    """Remplissage spécial pour fusionner les blocs du motif Sans."""
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            if is_obstacle(cell):
                rx, ry = x * 2 + 1, y * 2 + 1
                if cell.is_blocked:
                    char = "W"
                else:
                    if cell.sans_eye:
                        char = "Y"
                    else:
                        char = "O"
                output_grid[ry][rx] = char
                output_grid[ry][rx + 1] = char
                output_grid[ry + 1][rx] = char
                output_grid[ry + 1][rx + 1] = char

                if x + 1 < width and (
                    (cell.is_blocked and grid[x + 1][y].is_blocked)
                    or (cell.in_symbol and grid[x + 1][y].in_symbol)
                    or (cell.sans_eye and grid[x + 1][y].sans_eye)
                ):
                    output_grid[ry][rx + 2] = char
                    output_grid[ry + 1][rx + 2] = char

                if y + 1 < height and (
                    (cell.is_blocked and grid[x][y + 1].is_blocked)
                    or (cell.in_symbol and grid[x][y + 1].in_symbol)
                    or (cell.sans_eye and grid[x][y + 1].sans_eye)
                ):
                    output_grid[ry + 2][rx] = char
                    output_grid[ry + 2][rx + 1] = char


def render_terminal_blocks(
        matrix: List[List[str]],
        render_w: int,
        render_h: int,
        bg_list: List[str]) -> None:
    """This function is the one who is rendering the maze using ANSI code,
    with the color palette selected in the 'themes.py' file
    W: Wall
    B: Blocked (Border of the pattern)
    C: Core (The color of the pattern)
    I: Eye (Used exclusivly for the sans. pattern)
    .: The shortest opath from entry to exit
    M: The entry of the maze
    N: The exit of the maze"""
    color_map: Dict[str, str] = {
        "W": bg_list[0],
        "B": bg_list[1],
        "C": bg_list[2],
        "I": "\033[48;2;71;130;201m",
        ".": bg_list[4],
        "M": "\033[48;2;60;115;210m",
        "N": "\033[48;2;210;120;20m",
    }
    default_color = bg_list[3]
    reset_code = "\033[0m"
    for y in range(render_h):
        line = "".join(
            f"{color_map.get(matrix[y][x], default_color)}  {reset_code}"
            for x in range(render_w)
        )
        print(line)


def run_session(parsed: NamedTuple, new_gen: Tuple[List[List[str]], int, int, bool, List[str]]) -> None:
    matrix, r_w, r_h, is_sans, bg_list = new_gen
    theme_index: int = 0
    show_path: bool = True
    try:
        while True:
            print("1 - Re-generate Maze")
            print("2 - Show/hide path")
            print("3 - Change colour")
            print("q - Quit")
            choice = input("Select an option: ")
            if choice == "1":
                matrix, r_w, r_h, is_sans, _ = wilson_main(parsed)
                bg_list = get_bg_list_for_pattern(is_sans, theme_index)
            elif choice == "2":
                show_path = not show_path
            elif choice == "3":
                theme_index += 1
                bg_list = get_bg_list_for_pattern(is_sans, theme_index)
            elif choice == "q":
                sys.exit(0)
            else:
                print("Warning: learn to read options. Try again.", file=sys.stderr)
            temp: List[str] = bg_list.copy()
            if not show_path:
                temp[4] = temp[3]
            subprocess.run("clear")
            render_terminal_blocks(matrix, r_w, r_h, temp)
    except (EOFError, KeyboardInterrupt):
        exit_program("Exiting program properly.")

def wilson_main(parsed: NamedTuple) -> Tuple[List[List[str]], int, int, bool, List[str]]:
    """Main function to generate the maze and the path"""
    width, height, pattern = parsed.width, parsed.height, parsed.pattern
    maze, is_sans, bg_list = generate_wilson(width, height, pattern, parsed)
    matrix, r_w, r_h = build_matrix_1x1(maze, width, height, is_sans=is_sans)
    path = solve_dijkstra(maze, parsed)
    mark_path_in_matrix(matrix, path, parsed)
    render_terminal_blocks(matrix, r_w, r_h, bg_list)
    return matrix, r_w, r_h, is_sans, bg_list
