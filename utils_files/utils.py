from typing import IO, Generator


def nonblank_lines(file_object: IO[str]) -> Generator[str, None, None]:
    """
    Yields non-blank lines from a text file object,
    stripped of trailing whitespace

    Args:
        file_object: an open, readable text file object

    Yields:
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
                       pattern_w: int) -> dict[str, int]:
    """
    Getting the pattern coordinates

    Args:
        height: parsed grid height
        width: parsed grid width
        pattern_h: pattern's height
        pattern_w: pattern's width

    Returns:
        A dict with start_x, start_y, end_x, end_y
        End_x and end_y are exclusive upper bounds (the pattern
        occupies [start_x, end_x] and [start_x, end_y])
    """
    keys: list[str] = ["start_x", "start_y", "end_x", "end_y"]
    start_x: int = (width - pattern_w) // 2
    start_y: int = (height - pattern_h) // 2
    end_x: int = start_x + pattern_w
    end_y: int = start_y + pattern_h
    coords: list[int] = [start_x, start_y, end_x, end_y]
    coords_pattern: dict[str, int] = {}
    for i, key in enumerate(keys):
        coords_pattern[key] = coords[i]
    return coords_pattern
