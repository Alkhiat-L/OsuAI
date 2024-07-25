SHELL := /bin/bash

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

test: init
	pytest tests

.PHONY: init test start