# Detect OS
OS := $(shell uname 2>/dev/null || echo Windows)

# Virtual environment folder (same for all OS)
VENV = .venv

# Python and pip paths depending on OS
ifeq ($(OS), Windows)
    PYTHON = python
    PIP = $(VENV)/Scripts/pip
    FASTAPI = $(VENV)/Scripts/fastapi
else
    PYTHON = python3
    PIP = $(VENV)/bin/pip
    FASTAPI = $(VENV)/bin/fastapi
endif

default: install run

# Create virtual environment if missing
$(VENV):
	@if [ ! -d $(VENV) ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(FASTAPI) dev app/main.py --port 8080
