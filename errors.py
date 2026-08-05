import sys
from typing import NoReturn


def exit_program(error_message: str) -> NoReturn:
    print(error_message)
    sys.exit(1)
