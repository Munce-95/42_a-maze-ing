# ===== CACHES ===== #

RM_CACHE = rm -rf .mypy_cache .pytest_cache
RM_PYCACHE = find . -type d -name "__pycache__" -exec rm -rf {} +
RM_PYC = find . -type f -name "*.pyc" -delete
RM_OUTPUT = rm -f output_file.txt
RM_BUILD = rm -rf build dist mazegen.egg-info

# ===== COMPILATION ===== #

P3 = python3
MP = mypy .
MPS = mypy --strict .
F8 = flake8 .
FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# ===== DIRECTORIES AND FILES ===== #

FILE = a_maze_ing.py
CONF = config.txt
BUILD_VENV = .build-venv

# ===== RULES ===== #

all: run

run:
	@clear
	$(P3) $(FILE) $(CONF)

debug:
	@clear
	$(P3) -m pdb $(FILE) $(CONF)

lint:
	@clear
	@echo "Testing flake8"
	$(F8)
	@echo "Testing mypy"
	$(MP) $(FLAGS)

lint-strict:
	@clear
	@echo "Testing flake8"
	$(F8)
	@echo "Testing mypy --strict"
	$(MPS)

install:
	@clear
	@echo "No requirements to install"

package:
	@clear
	@echo "Building mazegen in an isolated venv..."
	$(P3) -m venv $(BUILD_VENV)
	./$(BUILD_VENV)/bin/pip install --quiet --upgrade pip build
	./$(BUILD_VENV)/bin/python3 -m build --wheel
	@echo "Built package available in dist/"

clean:
	@clear
	@echo "Cleaning temporary files..."
	$(RM_CACHE)
	$(RM_PYCACHE)
	$(RM_PYC)
	$(RM_OUTPUT)
	$(RM_BUILD)
	rm -rf $(BUILD_VENV)
	@echo "Clean done."

.PHONY: all run debug lint lint-strict install package clean