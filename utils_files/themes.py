from typing import NamedTuple, List
import random

BG_CORE = "\033[48;2;255;255;255m"

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
    name: str

THEMES = [
    Theme(RGB(42, 42, 42), RGB(85, 60, 100), RGB(200, 200, 200), "b/w"),
    Theme(RGB(50, 5, 85), RGB(253, 0, 219), RGB(100, 30, 90), "pink"),
    Theme(RGB(15, 23, 42), RGB(6, 182, 212), RGB(241, 245, 249), "trita"),
    Theme(RGB(10, 10, 10), RGB(20, 80, 20), RGB(100, 255, 100), "white"),
    Theme(RGB(0, 75, 15), RGB(10, 130, 30), RGB(210, 10, 175), "matrix"),
    Theme(RGB(0, 0, 0), RGB(255, 255, 255), RGB(57, 56, 82), "sans.")
]

def get_bg_list_for_pattern(pattern: List[List[int]], is_sans_pattern: bool) -> List[str]:
    if is_sans_pattern:
        current_theme = next(t for t in THEMES if t.name == "sans.")
    else:
        available_themes = [t for t in THEMES if t.name != "sans."]
        current_theme = random.choice(available_themes)
    return [
        current_theme.wall.to_ansi(),
        current_theme.logo.to_ansi(),
        BG_CORE,
        current_theme.path.to_ansi()
    ]