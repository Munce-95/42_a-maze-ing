import heapq
from typing import List, NamedTuple
from utils_files.cell import Cell


def get_dijkstra_neighbors(
        grid: List[List[Cell]],
        cell: Cell,
        parsed: NamedTuple) -> List[Cell]:
    neighbors = []
    x, y = cell.x, cell.y
    if not cell.walls['N'] and y > 0:
        neighbors.append(grid[x][y - 1])
    if not cell.walls['S'] and y < parsed.height - 1:
        neighbors.append(grid[x][y + 1])
    if not cell.walls['E'] and x < parsed.width - 1:
        neighbors.append(grid[x + 1][y])
    if not cell.walls['W'] and x > 0:
        neighbors.append(grid[x - 1][y])
    return neighbors


def solve_dijkstra(
        grid: List[List[Cell]],
        parsed: NamedTuple) -> List[Cell]:
    start_cell = grid[parsed.entry[0]][parsed.entry[1]]
    end_cell = grid[parsed.exit_[0]][parsed.exit_[1]]
    distances = {(c.x, c.y): float('inf') for row in grid for c in row}
    predecessors = {}
    distances[(start_cell.x, start_cell.y)] = 0
    pq = [(0, start_cell.x, start_cell.y)]

    while pq:
        current_dist, x, y = heapq.heappop(pq)
        current = grid[x][y]
        if current == end_cell:
            break
        if current_dist > distances[(x, y)]:
            continue
        for neighbor in get_dijkstra_neighbors(grid, current, parsed):
            new_dist = current_dist + 1
            if new_dist < distances[(neighbor.x, neighbor.y)]:
                distances[(neighbor.x, neighbor.y)] = new_dist
                predecessors[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor.x, neighbor.y))
    path = []
    curr = end_cell
    while curr in predecessors:
        path.append(curr)
        curr = predecessors[curr]
    if path or end_cell == start_cell:
        path.append(start_cell)
    return path[::-1]


def mark_path_in_matrix(
        matrix: List[List[str]],
        path: List[Cell],
        parsed: NamedTuple) -> None:
    for i in range(len(path)):
        cell = path[i]
        rx, ry = cell.x * 2 + 1, cell.y * 2 + 1
        matrix[ry][rx] = "."
        matrix[parsed.entry[1] * 2 + 1][parsed.entry[0] * 2 + 1] = "M"
        matrix[parsed.exit_[1] * 2 + 1][parsed.exit_[0] * 2 + 1] = "N"
        if i < len(path) - 1:
            next_cell = path[i + 1]
            mid_x = (rx + (next_cell.x * 2 + 1)) // 2
            mid_y = (ry + (next_cell.y * 2 + 1)) // 2
            matrix[mid_y][mid_x] = "."
