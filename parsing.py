import sys
import os
from typing import Any, Tuple, List, Dict
from utils_files import (nonblank_lines,
                         get_coords_pattern,
                         Data,
                         get_pattern_by_name)


MIN_DISPLAY_SIZE = 10


def check_args() -> None:
    """
    Is there only one argument? Does the file passed as argv[1] exist?

    Raises
    ------
    ValueError
        if the number of arguments is different than 2
    FileNotFoundError
        if the provided <config_file> doesn't exist
    IsADirectoryError
        if <config_file> is a directory
    """
    if len(sys.argv) != 2:
        raise ValueError("Error: there must be only one argument!\n"
                         "Usage: python3 a_maze_ing.py <config_file>.")
    if not os.path.exists(sys.argv[1]):
        raise FileNotFoundError(f"Error: file '{sys.argv[1]}' does not exist.")
    if not os.path.isfile(sys.argv[1]):
        raise IsADirectoryError(f"Error: '{sys.argv[1]}' is a directory.")
    if sys.argv[1] != "config.txt":
        raise ValueError("Error: the argument must be 'config.txt'")


def retrieve_raw_data(config_file: str) -> Dict[str, Any]:
    """
    Retrieving data from <config_file> provided by user (argv[1])

    Parameters
    ----------
    config_file : str
        file provided with argv[1]

    Returns
    -------
    Dict[str, Any]
        A dict with the retrieved data from <config_file>

    Raises
    ------
    KeyError
        if a key starts with a space
    ValueError
        if there is more than one key/value pair per line
    ValueError
        if <config_file> is not valid text
    PermissionError
        if <config_file> doesn't have the proper permission
    """
    raw_config: Dict[str, Any] = {}
    try:
        with open(config_file) as f:
            for line in nonblank_lines(f):
                if line.startswith('#'):
                    continue
                elif line.startswith(' '):
                    raise KeyError("Error: keys cannot start with a space.")
                elif line.count('=') > 1:
                    raise ValueError("Error: there can only be one"
                                     " key/value pair per line.")
                elif line.count('=') == 0:
                    raise ValueError("Error: key/value pair must be"
                                     "seperated by a '='.")
                else:
                    key, value = line.split('=', 1)
                    if key.upper().strip() in raw_config:
                        continue
                    else:
                        raw_config.update({key.upper().strip(): value.strip()})
    except UnicodeDecodeError:
        raise ValueError("Error: config file is not valid text.")
    except PermissionError:
        raise PermissionError("Error: permission denied.")
    return raw_config


def check_raw_data(raw_config: Dict[str, Any]) -> None:
    """
    Checking the data prior any mutation

    Parameters
    ----------
    raw_config : Dict[str, Any]
        A dict made out of the data from <config_file>

    Raises
    ------
    ValueError
        if at least 6 keys are not present
    KeyError
        if keys are commented or not written using letters/underscores
    KeyError
        if one of the mandatory keys is missing
    """
    if len(raw_config) < 6:
        raise ValueError("Error: there must be at least 6 keys"
                         " in the <config_file>.")

    for key in raw_config.keys():
        for c in key:
            if not (c.isalpha() or c == '_'):
                raise KeyError("Error: Keys must be written using"
                               " letters and not be commented.")

    mandatory_keys: List[str] = \
        ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in mandatory_keys:
        if key not in raw_config:
            raise KeyError("Error: one or more mandatory key(s) missing.")


def _check_dimensions(dict_config: Dict[str, Any]) -> Tuple[int, int]:
    """
    Checking that WIDTH and HEIGHT are valid integers.

    Parameters
    ----------
    dict_config : dict[str, Any]
        The config data being validated.

    Returns
    -------
    Tuple[int, int]
        A tuple holding WIDTH and HEIGHT.

    Raises
    ------
    ValueError
        If WIDTH and HEIGHT are not valid integers, or not between
        2 and 50.
    """
    try:
        width: int = int(dict_config["WIDTH"])
        dict_config.update({"WIDTH": width})
        height: int = int(dict_config["HEIGHT"])
        dict_config.update({"HEIGHT": height})
    except (TypeError, ValueError):
        raise ValueError("Error: WIDTH and HEIGHT must"
                         " be valid integers in <config_file>.")
    if not 2 <= width <= 50 or not 2 <= height <= 50:
        raise ValueError("Error: WIDTH and HEIGHT must be"
                         " >= 2 and <= 50 in <config_file>.")
    return (dict_config["WIDTH"], dict_config["HEIGHT"])


def _check_perfect(dict_config: Dict[str, Any]) -> None:
    """
    Checking that PERFECT accepts true or false and make it a boolean

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated

    Raises
    ------
    ValueError
        if <value> for PERFECT is anything else than true/false
    """
    perfect: str = dict_config.get("PERFECT", "").lower()
    if perfect not in ("true", "false"):
        raise ValueError("Error: PERFECT must be 'True' or"
                         " 'False' in <config_file>.")
    dict_config["PERFECT"] = perfect == "true"


def _check_output_file(dict_config: Dict[str, Any]) -> None:
    """
    Making sure the output file is a .txt

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated

    Raises
    ------
    ValueError
        if <output_file> doesn't end with .txt
    """
    output: str = dict_config["OUTPUT_FILE"]
    if not output.endswith(".txt"):
        raise ValueError("Error: <OUTPUT_FILE> should be a .txt")
    if output == "config.txt":
        raise ValueError("Error: why would you try this...?")
    dict_config.update({"OUTPUT_FILE": output})


def _check_entry_format(dict_config: Dict[str, Any]) -> Tuple[int, int]:
    """
    Checking that ENTRY has 2 valid integers

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated

    Returns
    -------
    Tuple[int, int]
        A Tuple holding ENTRY coordinates

    Raises
    ------
    ValueError
        if (x,y) format is not respected
    ValueError
        if ENTRY is not valid integers
    """
    values = dict_config["ENTRY"].split(',', 1)
    if len(values) != 2:
        raise ValueError("Error: format for ENTRY must be <ENTRY=x, y>.")
    try:
        entry_coords: Tuple[int, int] = (int(values[0]), int(values[1]))
        dict_config.update({"ENTRY": entry_coords})
    except ValueError:
        raise ValueError("Error: Values for ENTRY must be valid integers.")
    return entry_coords


def _check_exit_format(dict_config: Dict[str, Any]) -> Tuple[int, int]:
    """
    Checking that EXIT has 2 valid integers

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated

    Returns
    -------
    Tuple[int, int]
        A Tuple holding EXIT coordinates

    Raises
    ------
    ValueError
        if (x,y) format is not respected
    ValueError
        if EXIT is not valid integers
    """
    values = dict_config["EXIT"].split(',', 1)
    if len(values) != 2:
        raise ValueError("Error: format for EXIT must be <EXIT=x, y>.")
    try:
        exit_coords: Tuple[int, int] = (int(values[0]), int(values[1]))
        dict_config.update({"EXIT": exit_coords})
    except ValueError:
        raise ValueError("Error: Values for EXIT must be valid integers.")
    return exit_coords


def _check_entry_exit_bound(width_height: Tuple[int, int],
                            entry_coords: Tuple[int, int],
                            exit_coords: Tuple[int, int]) -> None:
    """
    Checking that ENTRY and EXIT are within the grid

    Parameters
    ----------
    width_height : Tuple[int, int]
        previously generated Tuple with WIDTH and HEIGHT
    entry_coords : Tuple[int, int]
        ENTRY coordinates (x,y)
    exit_coords : Tuple[int, int]
        EXIT coordinates (x,y)

    Raises
    ------
    ValueError
        if ENTRY or EXIT are set outside the grid
    """
    if not (0 <= entry_coords[0] < width_height[0]) \
        or not (0 <= entry_coords[1] < width_height[1]) \
            or not (0 <= exit_coords[0] < width_height[0]) \
            or not (0 <= exit_coords[1] < width_height[1]):
        raise ValueError("Error: ENTRY and EXIT must be within the grid.")


def _check_entry_exit_equality(entry_coords: Tuple[int, int],
                               exit_coords: Tuple[int, int]) -> None:
    """
    Making sure ENTRY and EXIT are different

    Parameters
    ----------
    entry_coords : Tuple[int, int]
        ENTRY coordinates (x,y)
    exit_coords : Tuple[int, int]
        EXIT coordinates (x,y)

    Raises
    ------
    ValueError
        if ENTRY and EXIT are the same
    """
    if entry_coords == exit_coords:
        raise ValueError("Error: ENTRY and EXIT cannot be the same.")


def _check_pattern_inclusion(dict_config: Dict[str, Any]) -> str:
    """
    Check if a specific pattern has been selected in config_file

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated

    Returns
    -------
    str
        The name of the selected pattern
        (defaults to 42 if none is selected or if more than one is True)
    """
    patterns: List[str] = ["PATTERN_PENGUIN",
                           "PATTERN_HEART",
                           "PATTERN_CEL",
                           "PATTERN_MATT",
                           "PATTERN_SANS"]
    true_keys: List[str] = [k for k in patterns
                            if dict_config.get(k, "false").lower() == "true"]
    pattern: str = ""
    if len(true_keys) == 0 or len(true_keys) > 1:
        pattern = "PATTERN_42"
        dict_config.update({"PATTERN": pattern})
    elif len(true_keys) == 1:
        pattern = true_keys[0]
        dict_config.update({"PATTERN": pattern})
    return pattern


def _check_pattern_displayable(width_height: Tuple[int, int],
                               entry_coords: Tuple[int, int],
                               exit_coords: Tuple[int, int],
                               pattern: str) -> None:
    """
    Is pattern displayable? Are both ENTRY and EXIT outside pattern?

    Parameters
    ----------
    width_height : Tuple[int, int]
        previously generated Tuple with WIDTH and HEIGHT
    entry_coords : Tuple[int, int]
        ENTRY coordinates (x,y)
    exit_coords : Tuple[int, int]
        EXIT coordinates (x,y)
    pattern : str
        previously selected pattern (or 42 by default)

    Raises
    ------
    ValueError
        if ENTRY or EXIT are inside the pattern
    """
    if width_height[1] < MIN_DISPLAY_SIZE \
       or width_height[0] < MIN_DISPLAY_SIZE:
        print("Warning: the grid is too small to display the pattern",
              file=sys.stderr)
    else:
        pattern_matrix: List[List[int]] = get_pattern_by_name(pattern)
        pattern_h: int = len(pattern_matrix)
        pattern_w: int = len(pattern_matrix[0])
        coords: Dict[str, int] = \
            get_coords_pattern(width_height[1],
                               width_height[0],
                               pattern_h,
                               pattern_w)
        if (coords["start_x"] <= entry_coords[0] < coords["end_x"]
            and coords["start_y"] <= entry_coords[1] < coords["end_y"]) \
                or (coords["start_x"] <= exit_coords[0] < coords["end_x"]
                    and coords["start_y"] <= exit_coords[1] < coords["end_y"]):
            raise ValueError(f"Error: values for ENTRY and"
                             f" EXIT must be outside"
                             f" ({coords['start_x']}, {coords['start_y']})"
                             f" and ({coords['end_x']}, {coords['end_y']})")


def _check_seed(dict_config: Dict[str, Any]) -> None:
    """
    Checking that SEED, if present, is a valid integer. Defaults to
    a fixed value if omitted, so generation is always reproducible.

    Parameters
    ----------
    dict_config : Dict[str, Any]
        Config data being validated

    Raises
    ------
    ValueError
        if SEED is present but not a valid integer
    """
    seed_str = dict_config.get("SEED", "42")
    try:
        dict_config["SEED"] = int(seed_str)
    except (TypeError, ValueError):
        raise ValueError("Error: SEED must be a valid integer.")


def check_values(dict_config: Dict[str, Any]) -> None:
    """
    Orchestrator for the whole parsing

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated
    """
    width_height: Tuple[int, int] = _check_dimensions(dict_config)
    _check_perfect(dict_config)
    _check_output_file(dict_config)
    entry_coords: Tuple[int, int] = _check_entry_format(dict_config)
    exit_coords: Tuple[int, int] = _check_exit_format(dict_config)
    _check_entry_exit_bound(width_height, entry_coords, exit_coords)
    _check_entry_exit_equality(entry_coords, exit_coords)
    pattern: str = _check_pattern_inclusion(dict_config)
    _check_pattern_displayable(width_height,
                               entry_coords, exit_coords, pattern)
    _check_seed(dict_config)


def get_parsed_values(dict_config: Dict[str, Any]) -> Data:
    """
    Retrieving parsed values from dict and constructing an instance of Data

    Parameters
    ----------
    dict_config : Dict[str, Any]
        The config data being validated

    Returns
    -------
    Data
        Data Class which takes a NamedTuple
    """
    parsed_values = Data(dict_config["WIDTH"],
                         dict_config["HEIGHT"],
                         dict_config["ENTRY"],
                         dict_config["EXIT"],
                         dict_config["OUTPUT_FILE"],
                         dict_config["PERFECT"],
                         dict_config["SEED"],
                         dict_config["PATTERN"])
    return parsed_values
