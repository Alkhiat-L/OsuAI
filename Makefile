PIP=uv pip

init:
	$(PIP) install -r requirements.txt

test:
	pytest tests

.PHONY: init test