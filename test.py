import random
import rich
from rich import print

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]

PATTERN_HEART = [
	[0, 1, 1, 0, 1, 1, 0],
	[1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1],
	[0, 1, 1, 1, 1, 1, 0],
	[0, 0, 1, 1, 1, 0, 0],
	[0, 0, 0, 1, 0, 0, 0]
]

PATTERN_PENGUIN = [
	[0, 0, 1, 1, 1, 0, 0],
	[0, 1, 0, 0, 0, 1, 0],
	[0, 1, 1, 0, 1, 1, 0],
	[1, 1, 0, 1, 0, 1, 1],
	[0, 1, 0, 0, 0, 1, 0],
	[0, 1, 1, 1, 1, 1, 0],
	[0, 0, 1, 0, 1, 0, 0]
]


class DisjointSet:
    def __init__(self):
        self.parent = {}

    def make_set(self, item):
        self.parent[item] = item

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        
        if root1 != root2:
            self.parent[root1] = root2
            return True
        return False


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.is_blocked = False


def remove_wall(cell1: Cell, cell2: Cell):
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


def apply_42_pattern(grid, width: int, height: int):
    pat_h = len(PATTERN_42)
    pat_w = len(PATTERN_42[0])
    
    start_x = (width - pat_w) // 2
    start_y = (height - pat_h) // 2

    for py in range(pat_h):
        for px in range(pat_w):
            if PATTERN_42[py][px] == 1:
                grid[start_x + px][start_y + py].is_blocked = True


def generate_kruskal(width: int, height: int):
    grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
    
    apply_42_pattern(grid, width, height)

    ds = DisjointSet()
    edges = []

    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            
            if cell.is_blocked:
                continue

            ds.make_set(cell)

            if x + 1 < width and not grid[x + 1][y].is_blocked:
                edges.append((cell, grid[x + 1][y]))
                
            if y + 1 < height and not grid[x][y + 1].is_blocked:
                edges.append((cell, grid[x][y + 1]))

    random.shuffle(edges)

    for cell1, cell2 in edges:
        if ds.union(cell1, cell2):
            remove_wall(cell1, cell2)

    return grid


def print_maze_ascii(grid, width, height):
    output = "+" + "---+" * width + "\n"

    for y in range(height):
        top_line = "|"
        bottom_line = "+"

        for x in range(width):
            cell = grid[x][y]

            if cell.is_blocked:
                top_line += "###"
            else:
                top_line += "   " 
            
            if x == width - 1:
                top_line += "|"
            elif cell.walls['E']:
                top_line += "|"
            else:
                top_line += " "

            if cell.walls['S']:
                bottom_line += "---"
            else:
                bottom_line += "   "
            
            bottom_line += "+"

        output += top_line + "\n"
        output += bottom_line + "\n"

    print(output)


if __name__ == "__main__":
    WIDTH, HEIGHT = 20, 20
    maze = generate_kruskal(WIDTH, HEIGHT)
    print_maze_ascii(maze, WIDTH, HEIGHT)