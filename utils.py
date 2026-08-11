from typing import IO, Generator


def nonblank_lines(file_object: IO[str]) -> Generator[str, None, None]:
    for lines in file_object:
        line = lines.rstrip()
        if line:
            yield line


def get_coords_pattern(height: int,
                       width: int,
                       pattern_h: int,
                       pattern_w: int) -> dict[str, int]:
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


if __name__ == "__main__":
    get_coords_pattern(20, 20, 7, 6)
