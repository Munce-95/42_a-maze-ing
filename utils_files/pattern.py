from typing import List, Dict

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0]
]

PATTERN_HEART = [
    [0, 1, 1, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0]
]

PATTERN_PENGUIN = [
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 2, 2, 1, 0],
    [0, 1, 2, 1, 2, 1, 2, 1, 0],
    [0, 1, 2, 2, 1, 2, 2, 1, 0],
    [1, 1, 2, 2, 2, 2, 2, 1, 1],
    [0, 1, 2, 2, 2, 2, 2, 1, 0],
    [0, 0, 1, 2, 1, 2, 1, 0, 0]
]

PATTERN_CEL = [
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0]
]

PATTERN_MATT = [
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0]
]

PATTERN_SANS = [
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 1, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 1],
    [1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 1, 2, 2, 1],
    [1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 1, 2, 2, 1],
    [0, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 0],
    [0, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 0],
    [1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1],
    [1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1],
    [1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [0, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0],
    [0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
]

pattern_list = [
    PATTERN_42,
    PATTERN_HEART,
    PATTERN_PENGUIN,
    PATTERN_CEL,
    PATTERN_MATT,
    PATTERN_SANS]

pattern_name: List[str] = [
    "PATTERN_42",
    "PATTERN_HEART",
    "PATTERN_PENGUIN",
    "PATTERN_CEL",
    "PATTERN_MATT",
    "PATTERN_SANS"]

pattern_dict: Dict[str, List[List[int]]] = {}
for i, pattern in enumerate(pattern_list):
    pattern_dict.update({pattern_name[i]: pattern})


def get_pattern_by_name(parsed_pattern: str) -> List[List[int]]:
    """
    Retrieve a pattern's matrix by its name

    Args:
        parsed_pattern: validated pattern's name from the <config_file>,
        can be 42 by default

    Returns:
        The selected pattern's matrix
    """
    return pattern_dict[parsed_pattern]
