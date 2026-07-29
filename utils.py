from typing import IO, Generator


def nonblank_lines(file_object: IO[str]) -> Generator[str, None, None]:
    for l in file_object:
        line = l.rstrip()
        if line:
            yield line
