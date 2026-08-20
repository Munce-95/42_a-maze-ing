import sys
from typing import NoReturn


def exit_program(error_message: str) -> NoReturn:
    """
    Printing an error message and killing the program

    Args:
        error_message: message to be printed
    """
    print(error_message)
    sys.exit(1)
