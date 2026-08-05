import random
from typing import List, Tuple
from utils_files.pattern import pattern_list
from utils_files.themes import bg_list


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
        width: int, height: int) -> None:
    pattern = random.choice(pattern_list)
    pat_h = len(pattern)
    pat_w = len(pattern[0])
    start_x = (width - pat_w) // 2
    start_y = (height - pat_h) // 2
    for py in range(pat_h):
        for px in range(pat_w):
            if pattern[py][px] == 1:
                grid[start_x + px][start_y + py].is_blocked = True
            elif pattern[py][px] == 2:
                grid[start_x + px][start_y + py].in_symbol = True


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
                and not grid[nx][ny].in_symbol):
            neighbors.append(grid[nx][ny])
    return neighbors


def generate_wilson(
        width: int,
        height: int) -> List[List[Cell]]:
    grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
    apply_42_pattern(grid, width, height)
    unvisited = [
        grid[x][y] for x in range(width)
        for y in range(height)
        if not grid[x][y].is_blocked and not grid[x][y].in_symbol]
    if not unvisited:
        return grid
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
    return grid


def build_matrix_1x1(
        grid: List[List[Cell]],
        width: int,
        height: int) -> Tuple[List[List[str]], int, int]:
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
            else:
                output_grid[ry][rx] = " "
                if not cell.walls['E']:
                    output_grid[ry][rx + 1] = " "
                if not cell.walls['S']:
                    output_grid[ry + 1][rx] = " "
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
                line += bg_list[0] + "  " + "\033[0m"
            elif char == "L":
                line += bg_list[1] + "  " + "\033[0m"
            elif char == "O":
                line += bg_list[2] + "  " + "\033[0m"
            else:
                line += bg_list[3] + "  " + "\033[0m"
        print(line)


if __name__ == "__main__":
    WIDTH, HEIGHT = 20, 20
    maze = generate_wilson(WIDTH, HEIGHT)
    matrix, r_w, r_h = build_matrix_1x1(maze, WIDTH, HEIGHT)
    render_terminal_blocks(matrix, r_w, r_h)
