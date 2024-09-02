# Variables
VENV_DIR=venv
REQ_FILE=requirements.txt

# Create virtual environment
.PHONY: venv
venv:
	python3 -m venv $(VENV_DIR)

# Activate virtual environment and install dependencies
.PHONY: install
install: venv
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r $(REQ_FILE)

# Clean the virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)

# Recreate virtual environment and install dependencies
.PHONY: reinstall
reinstall: clean install
