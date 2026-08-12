import sys
import os
import typing
from utils_files.utils import nonblank_lines, get_coords_pattern
from utils_files.data import Data
from utils_files.pattern import pattern_list

MIN_DISPLAY_SIZE = 10


def check_args() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Error: there must be only one argument!\n"
                         "Usage: python3 a_maze_ing.py <config_file>.")
    if not os.path.exists(sys.argv[1]):
        raise FileNotFoundError(f"Error: file '{sys.argv[1]}' does not exist.")
    if not os.path.isfile(sys.argv[1]):
        raise IsADirectoryError(f"Error: '{sys.argv[1]}' is a directory.")


def retrieve_raw_data(config_file: str) -> dict[str, typing.Any]:
    raw_config: dict[str, typing.Any] = {}
    with open(config_file) as f:
        for line in nonblank_lines(f):
            if line.startswith('#'):
                continue
            elif line.startswith(' '):
                raise KeyError("Error: keys cannot start with a space.")
            elif line.count('=') > 1:
                raise ValueError("Error: there can only be one"
                                 " key/value pair per line.")
            else:
                key, value = line.split('=', 1)
                if key.upper().strip() in raw_config:
                    continue
                else:
                    raw_config.update({key.upper().strip(): value.strip()})
    return raw_config


def check_raw_data(raw_config: dict[str, typing.Any]) -> None:
    if len(raw_config) < 6:
        raise ValueError("Error: there must be at least 6 keys"
                         " in the <config_file>.")

    # checking that keys are only composed of letters or underscores
    for key in raw_config.keys():
        for c in key:
            if not (c.isalpha() or c == '_'):
                raise KeyError("Error: Keys must be written using"
                               " letters and not be commented.")

    # checking mandatory keys are in <config_file>
    mandatory_keys: list[str] = \
        ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in mandatory_keys:
        if key not in raw_config:
            raise KeyError("Error: one or more mandatory key(s) missing.")


def check_values(dict_config: dict[str, typing.Any]) -> None:
    try:
        width: int = int(dict_config["WIDTH"])
        dict_config.update({"WIDTH": width})
        height: int = int(dict_config["HEIGHT"])
        dict_config.update({"HEIGHT": height})
    except (TypeError, ValueError):
        raise ValueError("Error: WIDTH and HEIGHT must"
                         " be valid integers in <config_file>.")
    if not 3 <= width <= 50 or not 3 <= height <= 50:
        raise ValueError("Error: WIDTH and HEIGHT must be"
                         " >= 3 and <= 50 in <config_file>.")

    # checking that PERFECT only accepts "true" or
    # "false" and make it a boolean
    perfect: str = dict_config.get("PERFECT", "").lower()
    if perfect not in ("true", "false"):
        raise ValueError("Error: PERFECT must be 'True' or"
                         " 'False' in <config_file>.")
    dict_config["PERFECT"] = perfect == "true"

    # checking that the output file is a .txt
    output: str = dict_config["OUTPUT_FILE"]
    if not output.endswith(".txt"):
        raise ValueError("Error: <OUTPUT_FILE> should be a .txt")
    dict_config.update({"OUTPUT_FILE": output})

    # checking that ENTRY has 2 valid integers
    # and making them a tuple[int, int]
    values = dict_config["ENTRY"].split(',', 1)
    if len(values) != 2:
        raise ValueError("Error: format for ENTRY must be <entry=x, y>.")
    try:
        entry_coords: tuple[int, int] = (int(values[0]), int(values[1]))
        dict_config.update({"ENTRY": entry_coords})
    except ValueError:
        raise ValueError("Error: Values for ENTRY must be valid integers.")

    # checking that EXIT has 2 valid integers and making them a tuple[int, int]
    values = dict_config["EXIT"].split(',', 1)
    if len(values) != 2:
        raise ValueError("Error: format for EXIT must be <exit=x, y>.")
    try:
        exit_coords: tuple[int, int] = (int(values[0]), int(values[1]))
        dict_config.update({"EXIT": exit_coords})
    except ValueError:
        raise ValueError("Error: Values for EXIT must be valid integers.")

    # checking ENTRY and EXIT are within the grid
    if not (0 <= entry_coords[0] < width) \
        or not (0 <= entry_coords[1] < height) \
            or not (0 <= exit_coords[0] < width) \
            or not (0 <= exit_coords[1] < height):
        raise ValueError("Error: ENTRY and EXIT must be within the grid.")

    # checking ENTRY and EXIT are not at the same position
    if entry_coords == exit_coords:
        raise ValueError("Error: ENTRY and EXIT cannot be the same.")

    # checking if pattern is displayable
    if height < MIN_DISPLAY_SIZE or width < MIN_DISPLAY_SIZE:
        print("Warning: the grid is too small to display the pattern", file=sys.stderr)
    else:
        # making sure that ENTRY and EXIT are not
        # where the 42 pattern is going to be
        pattern_h: int = 7
        pattern_w: int = 6
        coords: dict[str, int] = \
            get_coords_pattern(height, width, pattern_h, pattern_w)
        if (coords["start_x"] <= entry_coords[0] < coords["end_x"]
        and coords["start_y"] <= entry_coords[1] < coords["end_y"]) \
        or (coords["start_x"] <= exit_coords[0] < coords["end_x"]
        and coords["start_y"] <= exit_coords[1] < coords["end_y"]):
            raise ValueError(f"Error: values for ENTRY and EXIT must be outside"
                            f" ({coords['start_x']}, {coords['start_y']})"
                            f" and ({coords['end_x']}, {coords['end_y']})")


def get_parsed_values(dict_config: dict[str, typing.Any]) -> Data:
    parsed_values = Data(dict_config["WIDTH"],
                         dict_config["HEIGHT"],
                         dict_config["ENTRY"],
                         dict_config["EXIT"],
                         dict_config["OUTPUT_FILE"],
                         dict_config["PERFECT"])
    return parsed_values



'''
need to add exclusion of a parameter if the first character of the line in config.txt is # - WIP
blank return lines to be ignored  - OK
key should always start first char on the line  string.startswith('') + put in README that it is deliberate for lines starting with spaces to raise an error - OK missing README
PERFECT should be boolean, not str - OK?
don't allow spaces before and after = and enforce .txt for OUTPUT_FILE and justify in readme.md
if grid is too small, 42 is omitted and an error message (to stderr) is printed stating that 42 could not be printed
add an upper limit to X (50)
in readme: state that < 3 creates a map that cannot be non-perfect
make sure format for ENTRY and EXIT is tuple -> X,Y - OK
ENTRY and EXIT must be inside the maze and must not be the same and must not be inside 42 - OK
the user cannot add or edit any parameter to config.txt
import signal to catch ctrl + c
if grid is < 8,6 -> error message to not display pattern

// Pour la selection de theme :
// Avoir une key "THEME" allant de 0 a nb_theme-1 (surement 5)
// 42 / Coeur / Pingouin / C / M / Sans
// Avec 0 == PATTERN_42
// Pour pouvoir naviguer plus tard entre les thèmes (?)
// Sauf si j'ai mal compris le fonctionnement du switch


pour le 42: WIDHT x HEIGHT
'''
