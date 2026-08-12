#!/usr/bin/env python3

import sys
import typing
from errors import exit_program
from parsing import check_raw_data, check_args, retrieve_raw_data, check_values
from wilson_maze_gen import wilson_main


def main() -> None:
    check_args()
    retrieved_data: dict[str, typing.Any] = retrieve_raw_data(sys.argv[1])
    check_raw_data(retrieved_data)
    check_values(retrieved_data)
    wilson_main(20, 20)
    



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
