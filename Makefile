# Makefile
SHELL = /bin/bash
VENV = .venv
PYTHON_VERSION = 3.12

# Colors for echos
ccend=$(shell tput sgr0)
ccso=$(shell tput smso)

python:
	pyenv install ${PYTHON_VERSION}

.ONESHELL:
venv:
	@echo ""
	@echo "$(ccso)--> Creating virtual environment $(ccend)"
	pyenv local ${PYTHON_VERSION}
	poetry install