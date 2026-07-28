import sys
import typing


def check_args() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Error: there must be only one argument!\n"
                         "Usage: python3 a_maze_ing.py <config_file>.")
    if sys.argv[1] != "config.txt":
        raise FileNotFoundError("Error: wrong name for <config_file>.")

    # add a function ft_error to exit the program after each raise / from typing import noreturn


def retrieve_raw_data(config_file: str) -> dict[str, typing.Any]:
    raw_config: dict[str, typing.Any] = {}
    with open(config_file) as f:
        for line in f:
            key, value = line.split('=', 1)
            raw_config.update({key.strip(): value.strip()})
    return raw_config


def check_raw_data(raw_config: dict[str, typing.Any]) -> None:
    if len(raw_config) < 6:
        raise ValueError("Error: there must be at least 6 keys"
                         "in the <config_file>.")
    mandatory_keys: list[str] = \
        ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in mandatory_keys:
        if key not in raw_config:
            raise KeyError("Error: one or more mandatory key(s) missing.")
    print(raw_config)
