import sys
import os.path
import typing
from utils_files.utils import nonblank_lines

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
            if line.startswith(' '):
                raise KeyError("Error: keys cannot start with a space.")
            elif line.count('=') > 1:
                raise ValueError("Error: there can only be one key/value pair per line.")
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
        height: int = int(dict_config["HEIGHT"])
    except (TypeError, ValueError):
        raise ValueError("Error: WIDTH and HEIGHT must"
                         " be valid integers in <config_file>.")
    if not 3 <= width <= 50 or not 3 <= height <= 50:
        raise ValueError("Error: WIDTH and HEIGHT must be"
                         " >= 3 and <= 50 in <config_file>.")

    perfect: str = dict_config.get("PERFECT", "").lower()
    if perfect not in ("true", "false"):
        raise ValueError("Error: PERFECT must be 'True' or"
                         " 'False' in <config_file>.")
    dict_config["PERFECT"] = perfect == "true"

    output: str = dict_config["OUTPUT_FILE"]
    if not output.endswith(".txt"):
        raise ValueError("Error: <OUTPUT_FILE> should be a .txt")

    x, y = dict_config["ENTRY"].split(',', 1).strip()
    print(x, y)
#        try:
#            x, y = dict_config["ENTRY"].split(',', 1).strip()
#            dict_config["ENTRY"] = tuple(x,y)
#        except ValueError:
#            raise ValueError("Error: ENTRY and EXIT must be tuple(int, int)")
#    try:
#        entry_tup: tuple[int, int] = tuple(dict_config["ENTRY"])
#        exit_tup: tuple[int, int] = tuple(dict_config["EXIT"])
#    except ValueError:
#        raise ValueError("Error: ENTRY and EXIT must be tuple[int, int]")
    



'''
need to add exclusion of a parameter if the first character of the line in config.txt is # - WIP
blank return lines to be ignored  - OK
key should always start first char on the line  string.startswith('') - OK
PERFECT should be boolean, not str - OK?
don't allow spaces before and after = and enforce .txt for OUTPUT_FILE and justify in readme.md
if grid is too small, 42 is omitted and an error message (to stderr) is printed stating that 42 could not be printed
add an upper limit to X (50)
in readme: state that < 3 creates a map that cannot be non-perfect
make sure format for ENTRY and EXIT is tuple -> X,Y
ENTRY and EXIT must be inside the maze and must not be the same and must not be inside 42
the user cannot add or edit any parameter to config.txt
import signal to catch ctrl + c
'''
