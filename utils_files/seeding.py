import random
from typing import NamedTuple


def apply_and_update_seed(parsed: NamedTuple, config_path: str = "config.txt") -> int:
    """Applique la seed de parsed.seed. Si elle est absente, en génère une et l'écrit dans le fichier config."""
    seed_value = parsed.seed

    # Si la seed est absente (None ou chaîne vide)
    if seed_value is None or str(seed_value).strip() == "":
        seed_value = random.randint(100000, 999999)
        _update_config_file_seed(config_path, seed_value)

    # Convertir en entier et initialiser la seed globalement
    seed_int = int(seed_value)
    random.seed(seed_int)
    return seed_int


def _update_config_file_seed(config_path: str, new_seed: int) -> None:
    """Met à jour uniquement la ligne SEED= dans le fichier de config."""
    with open(config_path, "r") as f:
        lines = f.readlines()

    seed_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("SEED="):
            lines[i] = f"SEED={new_seed}\n"
            seed_found = True
            break

    if not seed_found:
        lines.append(f"SEED={new_seed}\n")

    with open(config_path, "w") as f:
        f.writelines(lines)