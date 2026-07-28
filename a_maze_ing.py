#!/usr/bin/env python3

import sys
import typing
from parsing import check_raw_data, check_args, retrieve_raw_data


def main() -> None:
    check_args()
    retrieved_data: dict[str, typing.Any] = retrieve_raw_data(sys.argv[1])
    check_raw_data(retrieved_data)


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, FileNotFoundError) as e:
        print(e)
