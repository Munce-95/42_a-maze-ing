# ===== CACHES ===== #

RM_CACHE = rm -rf .mypy_cache .pytest_cache
RM_PYCACHE = find . -type d -name "__pycache__" -exec rm -rf {} +
RM_PYC = find . -type f -name "*.pyc" -delete
RM_OUTPUT = rm output_file.txt

# ===== COMPILATION ===== #

P3 = python3
MP = mypy .
MPS = mypy --strict .
F8 = flake8 .
FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# ===== DIRECTORIES AND FILES ===== #

FILE = a_maze_ing.py
CONF = config.txt

# ===== RULES ===== #

all: run

run:
	@echo "Running program"
	$(P3) $(FILE) $(CONF)

lint:
	@echo "Testing flake8"
	$(F8)
	@echo "Testing mypy"
	$(MP) $(FLAGS)

lint-strict:
	@echo "Testing flake8"
	$(F8)
	@echo "Testing mypy --strict"
	$(MPS)

install:
	@echo "No requirements to install"

clean:
	@echo "Cleaning temporary files..."
	$(RM_CACHE)
	$(RM_PYCACHE)
	$(RM_PYC)
	$(RM_OUTPUT)
	@echo "Clean done."

.PHONY: all run lint lint-strict install clean