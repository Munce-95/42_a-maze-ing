from typing import NamedTuple


class Data(NamedTuple):
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool