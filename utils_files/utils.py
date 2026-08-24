from typing import IO, Generator, Dict, List


def nonblank_lines(file_object: IO[str]) -> Generator[str, None, None]:
    """
    Yields non-blank lines from a text file object,
    stripped of trailing whitespace

    Parameters
    ----------
    file_object : IO[str]
        an open, readable text file object

    Yields
    ------
    str
        Each line with trailing whitespace removed,
        skipping any line that is empty or contains only whitespace
    """
    for lines in file_object:
        line = lines.rstrip()
        if line:
            yield line


def get_coords_pattern(height: int,
                       width: int,
                       pattern_h: int,
                       pattern_w: int) -> Dict[str, int]:
    """
    Getting the pattern coordinates

    Parameters
    ----------
    height : int
        parsed grid height
    width : int
        parsed grid width
    pattern_h : int
        pattern's height
    pattern_w : int
        pattern's width

    Returns
    -------
    Dict[str, int]
        A dict with start_x, start_y, end_x, end_y
        End_x and end_y are exclusive upper bounds (the pattern
        occupies [start_x, end_x] and [start_x, end_y])
    """
    keys: List[str] = ["start_x", "start_y", "end_x", "end_y"]
    start_x: int = (width - pattern_w) // 2
    start_y: int = (height - pattern_h) // 2
    end_x: int = start_x + pattern_w
    end_y: int = start_y + pattern_h
    coords: List[int] = [start_x, start_y, end_x, end_y]
    coords_pattern: Dict[str, int] = {}
    for i, key in enumerate(keys):
        coords_pattern[key] = coords[i]
    return coords_pattern
