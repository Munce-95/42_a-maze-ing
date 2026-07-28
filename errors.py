import sys
from typing import NoReturn


def exiting(error_message: str) -> NoReturn:
    print(error_message)
    sys.exit(1)
