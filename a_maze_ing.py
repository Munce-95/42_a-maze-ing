#!/usr/bin/env python3

import sys
import subprocess
import random
from typing import Tuple, List, Any
from errors import exit_program
from algorithms.wilson import wilson_main, run_session
from parsing import (
    check_raw_data,
    check_args,
    retrieve_raw_data,
    check_values,
    get_parsed_values)
from utils_files.data import Data


def main() -> None:
    check_args()
    retrieved_data: dict[str, Any] = retrieve_raw_data(sys.argv[1])
    check_raw_data(retrieved_data)
    check_values(retrieved_data)
    parsed: Data = get_parsed_values(retrieved_data)
    random.seed(parsed.seed)
    new_gen: Tuple[List[List[str]],
                   int,
                   int,
                   bool,
                   List[str]] = wilson_main(parsed)
    run_session(parsed, new_gen)


if __name__ == "__main__":
    try:
        subprocess.run("clear")
        main()
    except (TypeError,
            IsADirectoryError,
            KeyError,
            ValueError,
            FileNotFoundError,
            EOFError,
            KeyboardInterrupt) as e:
        exit_program(str(e))
    else:
        print("All good! ... for now")
