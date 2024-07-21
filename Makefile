SHELL := /bin/bash

PIP=uv pip

init:
	$(PIP) install -r requirements.txt

start: test init
	python -m osupy.OsuPy

test: init
	pytest tests

.PHONY: init test start