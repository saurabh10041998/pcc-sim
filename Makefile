.PHONY: all format

all:
	pip3 install -e .

format:
	black setup.py
	black cli/*.py
	black core/*.py