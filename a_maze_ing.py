#!/usr/bin/env python3

from parsing import *


def main() -> None:
    check_args()
    retrieve_data(sys.argv[1])
    check_data(retrieve_data(sys.argv[1]))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, FileNotFoundError) as e:
        print(e)
