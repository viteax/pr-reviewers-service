install:
	python3 -m venv .venv
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	.venv/bin/uvicorn main:app --reload

default: install run
