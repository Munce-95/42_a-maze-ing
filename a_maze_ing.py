#!/usr/bin/env python3

import sys
import typing
from errors import exit_program
from algorithms.wilson_maze_gen import wilson_main
from parsing import (
    check_raw_data,
    check_args,
    retrieve_raw_data,
    check_values,
    get_parsed_values)
from utils_files.data import Data


def main() -> None:
    # MATT PART :
    check_args()
    retrieved_data: dict[str, typing.Any] = retrieve_raw_data(sys.argv[1])
    check_raw_data(retrieved_data)
    check_values(retrieved_data)
    parsed: Data = get_parsed_values(retrieved_data)
    print(parsed.pattern)

    # CEL PART :
    wilson_main(parsed)


if __name__ == "__main__":
    try:
        main()
    except (TypeError,
            IsADirectoryError,
            KeyError,
            ValueError,
            FileNotFoundError) as e:
        exit_program(str(e))
    else:
        print("All good! ... for now")
