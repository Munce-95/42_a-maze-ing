from typing import NamedTuple
import random


COLOR_RESET = "\033[0m"
BG_CORE = "\033[48;2;255;255;255m"

bg_list = []

class RGB(NamedTuple):
    r: int
    g: int
    b: int

    def to_ansi(self) -> str:
        return f"\033[48;2;{self.r};{self.g};{self.b}m"

class Theme(NamedTuple):
    wall: RGB
    logo: RGB
    path: RGB

THEMES = [
    Theme(RGB(42, 42, 42), RGB(85, 60, 100), RGB(200, 200, 200)),
    Theme(RGB(50, 5, 85), RGB(253, 0, 219), RGB(100, 30, 90)),
    Theme(RGB(15, 23, 42), RGB(6, 182, 212), RGB(241, 245, 249)),
    Theme(RGB(10, 10, 10), RGB(20, 80, 20), RGB(100, 255, 100)),
    Theme(RGB(0, 75, 15), RGB(10, 130, 30), RGB(210, 10, 175))
]

current_theme = random.choice(THEMES)

BG_WALL = current_theme.wall.to_ansi()
BG_LOGO = current_theme.logo.to_ansi()
BG_PATH = current_theme.path.to_ansi()