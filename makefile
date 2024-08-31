# Makefile for managing Python scripts

# Variables
PYTHON = python
SCRIPT_NOUN_SEARCH = ./scripts/noun_search.py
SCRIPT_GENERATE = ./generate.py
INPUT_DIR = ./text
OUTPUT_FILE_NOUN_SEARCH = ./results/nouns.csv
OUTPUT_DIR_GENERATE = ./results/text
LOG_FILE = ./results/processed_files.log

# Default target
all: run-noun-search run-generate

# Run the noun_search.py script
run-noun-search:
	$(PYTHON) $(SCRIPT_NOUN_SEARCH) --input-dir $(INPUT_DIR) --output-file $(OUTPUT_FILE_NOUN_SEARCH)

# Run the generate.py script with API_URL passed as an argument
run-generate:
ifndef API_URL
	$(error API_URL is not defined. Please set it before running this target.)
endif
	$(PYTHON) $(SCRIPT_GENERATE) --apiurl $(API_URL) --input-dir $(INPUT_DIR) --output-dir $(OUTPUT_DIR_GENERATE) --log-file $(LOG_FILE)

# Clean up output directories and files
clean:
	rm -rf $(OUTPUT_FILE_NOUN_SEARCH) $(OUTPUT_DIR_GENERATE) $(LOG_FILE)

# Create virtual environment (if needed)
venv:
	$(PYTHON) -m venv venv
	./venv/bin/pip install -r requirements.txt

# Install dependencies (if using requirements.txt)
install:
	./venv/bin/pip install -r requirements.txt

# Activate virtual environment (for convenience)
activate:
	. venv/bin/activate
