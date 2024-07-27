PIP=uv pip

PYTHON=python

ifeq ($(OS),Windows_NT)
	PYTHON=.venv/Scripts/python
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		PYTHON=.venv/bin/python
	endif
endif

init:
	$(PIP) install -r requirements.txt

start: test init
	$(PYTHON) -m osupy.OsuPy

debug: test init
	$(PYTHON) -m debugpy --listen 5678 --wait-for-client -m osupy.OsuPy

env: test init
	$(PYTHON) -m osupy.env

test: init
	pytest tests

.PHONY: init test start