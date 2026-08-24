from typing import NamedTuple, List

BG_CORE = "\033[48;2;255;255;255m"


class RGB(NamedTuple):
    """
    An RGB colour, convertible to an ANSI background escape code

    Parameters
    ----------
    r : int
        red channel, 0-255
    g : int
        green channel, 0-255
    b : int
        blue channel, 0-255
    """
    r: int
    g: int
    b: int

    def to_ansi(self) -> str:
        """
        Returns
        -------
        str
            This colour as an ANSI background-colour escape sequence
        """
        return f"\033[48;2;{self.r};{self.g};{self.b}m"


class Theme(NamedTuple):
    """
    A named colour scheme for rendering the maze in the terminal

    Parameters
    ----------
    wall : RGB
        colour used for maze walls
    logo : RGB
        colour used for the pattern's outline/blocked cells
    path : RGB
        colour used for plain open-floor cells
    way : RGB
        colour used for the solved path's marked cells
    name : str
        the theme's identifier (e.g. "b/w", "pink", "sans.")
    """
    wall: RGB
    logo: RGB
    path: RGB
    way: RGB
    name: str


THEMES = [
    Theme(
        RGB(42, 42, 42),
        RGB(85, 60, 100),
        RGB(200, 200, 200),
        RGB(80, 80, 80), "b/w"),
    Theme(
        RGB(50, 5, 85),
        RGB(253, 0, 219),
        RGB(100, 30, 90),
        RGB(200, 70, 220), "pink"),
    Theme(
        RGB(15, 23, 42),
        RGB(6, 182, 212),
        RGB(241, 245, 249),
        RGB(110, 110, 110), "white"),
    Theme(
        RGB(10, 10, 10),
        RGB(20, 80, 20),
        RGB(100, 255, 100),
        RGB(0, 140, 42), "trita"),
    Theme(
        RGB(0, 75, 15),
        RGB(10, 130, 30),
        RGB(210, 10, 175),
        RGB(0, 255, 0), "matrix"),
    Theme(
        RGB(0, 0, 0),
        RGB(255, 255, 255),
        RGB(57, 56, 82),
        RGB(200, 194, 226), "sans.")
]


def get_bg_list_for_pattern(is_sans_pattern: bool,
                            theme_index: int = 0) -> List[str]:
    """
    Builds the list of ANSI colours used to render one maze frame

    If is_sans_pattern is True, always uses the fixed "sans." theme,
    ignoring theme_index. Otherwise, selects a theme from THEMES
    (excluding "sans.") by cycling through theme_index, wrapping
    around once every theme has been used

    Parameters
    ----------
    is_sans_pattern : bool
        whether the maze's selected pattern is SANS
    theme_index : int
        cycling index into the available (non-SANS)
        themes; wraps automatically via modulo

    Returns
    -------
    List[str]
        A 5-element list of ANSI escape codes, in order:
        [wall, logo, open-floor, path-default, solved-path]
    """
    if is_sans_pattern:
        current_theme = next(t for t in THEMES if t.name == "sans.")
    else:
        available_themes = [t for t in THEMES if t.name != "sans."]
        current_theme = available_themes[theme_index % len(available_themes)]
    return [
        current_theme.wall.to_ansi(),
        current_theme.logo.to_ansi(),
        BG_CORE,
        current_theme.path.to_ansi(),
        current_theme.way.to_ansi()
    ]
