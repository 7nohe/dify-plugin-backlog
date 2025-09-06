.PHONY: fmt lint test

venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip -r requirements.txt

fmt:
	. .venv/bin/activate && black .

lint:
	. .venv/bin/activate && ruff check .

test:
	. .venv/bin/activate && pytest -q
