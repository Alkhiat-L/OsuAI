PIP=uv pip

init:
	$(PIP) install -r requirements.txt

start: init
	python -m osupy.OsuPy

test:
	pytest tests

.PHONY: init test