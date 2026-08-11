from typing import IO, Generator


def nonblank_lines(file_object: IO[str]) -> Generator[str, None, None]:
    for lines in file_object:
        line = lines.rstrip()
        if line:
            yield line
