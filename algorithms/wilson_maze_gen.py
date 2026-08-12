import random
from typing import List, Tuple, NamedTuple
from utils_files.pattern import pattern_list, PATTERN_SANS, PATTERN_PENGUIN
from utils_files.themes import get_bg_list_for_pattern
from algorithms.dijkstra import solve_dijkstra, mark_path_in_matrix


current_bg_list: List[str] = []

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


def remove_wall(
        cell1: Cell,
        cell2: Cell) -> None:
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


def apply_42_pattern(
        grid: List[List[Cell]],
        width: int,
        height: int) -> bool:
    global current_bg_list
    pattern = random.choice(pattern_list)
    while (
            pattern == PATTERN_SANS and (width < 20 or height < 20)
            or (pattern == PATTERN_PENGUIN) and (width < 12 or height < 12)):
        if len(pattern_list) < 3:
            return f"Can't generate pattern"
        pattern = random.choice(pattern_list)
    is_sans = (pattern == PATTERN_SANS)
    current_bg_list = get_bg_list_for_pattern(pattern, is_sans)
    pat_h = len(pattern)
    pat_w = len(pattern[0])
    start_x = (width - pat_w) // 2
    start_y = (height - pat_h) // 2
    for py in range(pat_h):
        if (width < 10 or height < 10):
            break
        for px in range(pat_w):
            if pattern[py][px] == 1:
                grid[start_x + px][start_y + py].is_blocked = True
            elif pattern[py][px] == 2:
                grid[start_x + px][start_y + py].in_symbol = True
            elif pattern[py][px] == 3:
                grid[start_x + px][start_y + py].sans_eye = True
    return is_sans


def get_unblocked_neighbors(
        grid: List[List[Cell]],
        cell: Cell,
        width: int,
        height: int) -> List[Cell]:
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = cell.x + dx, cell.y + dy
        if (
                0 <= nx < width
                and 0 <= ny < height
                and not grid[nx][ny].is_blocked
                and not grid[nx][ny].in_symbol
                and not grid[nx][ny].sans_eye):
            neighbors.append(grid[nx][ny])
    return neighbors


def generate_wilson(
        width: int,
        height: int) -> List[List[Cell]]:
    grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
    is_sans = apply_42_pattern(grid, width, height)
    unvisited = [
        grid[x][y] for x in range(width)
        for y in range(height)
        if (
            not grid[x][y].is_blocked
            and not grid[x][y].in_symbol
            and not grid[x][y].sans_eye)]
    if not unvisited:
        return grid, is_sans
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
    return grid, is_sans


def build_matrix_1x1(
        grid: List[List[Cell]],
        width: int,
        height: int,
        is_sans: bool = False) -> Tuple[List[List[str]], int, int]:
    render_w = width * 2 + 1
    render_h = height * 2 + 1
    output_grid = [["#" for _ in range(render_w)] for _ in range(render_h)]
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            rx = x * 2 + 1
            ry = y * 2 + 1
            if cell.is_blocked:
                output_grid[ry][rx] = "L"
            elif cell.in_symbol:
                output_grid[ry][rx] = "O"
            elif cell.sans_eye:
                output_grid[ry][rx] = "Y"
            else:
                output_grid[ry][rx] = " "
                if not cell.walls['E']:
                    output_grid[ry][rx + 1] = " "
                if not cell.walls['S']:
                    output_grid[ry + 1][rx] = " "
    if is_sans:
        for x in range(width):
            for y in range(height):
                cell = grid[x][y]
                if cell.is_blocked or cell.in_symbol or cell.sans_eye:
                    rx = x * 2 + 1
                    ry = y * 2 + 1
                    if cell.is_blocked:
                        char = "#"
                    elif cell.sans_eye:
                        char = "Y"
                    else:
                        char = "O"
                    output_grid[ry][rx] = char
                    output_grid[ry][rx + 1] = char
                    output_grid[ry + 1][rx] = char
                    output_grid[ry + 1][rx + 1] = char
                    if x + 1 < width and (
                        (cell.is_blocked and grid[x + 1][y].is_blocked) or
                        (cell.in_symbol and grid[x + 1][y].in_symbol) or
                        (cell.sans_eye and grid[x + 1][y].sans_eye)
                    ):
                        output_grid[ry][rx + 2] = char
                        output_grid[ry + 1][rx + 2] = char
                    if y + 1 < height and (
                        (cell.is_blocked and grid[x][y + 1].is_blocked) or
                        (cell.in_symbol and grid[x][y + 1].in_symbol) or
                        (cell.sans_eye and grid[x][y + 1].sans_eye)
                    ):
                        output_grid[ry + 2][rx] = char
                        output_grid[ry + 2][rx + 1] = char
    return output_grid, render_w, render_h


def render_terminal_blocks(
        matrix: List[List[str]],
        render_w: int,
        render_h: int) -> None:
    for y in range(render_h):
        line = ""
        for x in range(render_w):
            char = matrix[y][x]
            if char == "#":
                line += current_bg_list[0] + "  " + "\033[0m"
            elif char == "L":
                line += current_bg_list[1] + "  " + "\033[0m"
            elif char == "O":
                line += current_bg_list[2] + "  " + "\033[0m"
            elif char == "Y":
                line += "\033[48;2;71;130;201m" + "  " + "\033[0m"
            elif char == ".":
                line += "\033[48;2;230;50;50m" + "  " + "\033[0m"
            else:
                line += current_bg_list[3] + "  " + "\033[0m"
        print(line)
    
def wilson_main(parsed: NamedTuple) -> None:
    WIDTH, HEIGHT = parsed.width, parsed.height
    maze, is_sans = generate_wilson(WIDTH, HEIGHT)
    matrix, r_w, r_h = build_matrix_1x1(maze, WIDTH, HEIGHT, is_sans=is_sans)
    path = solve_dijkstra(maze, parsed)
    mark_path_in_matrix(matrix, path)
    render_terminal_blocks(matrix, r_w, r_h)

if __name__ == "__main__":
    WIDTH, HEIGHT = 50, 50
    maze, is_sans = generate_wilson(WIDTH, HEIGHT)
    matrix, r_w, r_h = build_matrix_1x1(maze, WIDTH, HEIGHT, is_sans=is_sans)
    render_terminal_blocks(matrix, r_w, r_h)
