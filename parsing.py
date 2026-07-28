import sys, typing


def check_args() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Error: There must be only one argument!\nUsage: python3 a_maze_ing.py <config_file>.")
    if sys.argv[1] != "config.txt":
        raise FileNotFoundError(f"Error: Wrong name for <config_file>.")


def retrieve_data(config_file: str) -> dict[str, typing.Any]:
    dict_config: dict[str, typing.Any] = {}
    with open(config_file) as f:
        for line in f:
            key, value = line.split('=', 1)
            dict_config.update({key.strip(): value.strip()})
    return dict_config


def main() -> None:
    print(retrieve_data(sys.argv[1]))


if __name__ == "__main__":
    try:
        check_args()
    except (ValueError, FileNotFoundError) as e:
        print(e)

    main()
