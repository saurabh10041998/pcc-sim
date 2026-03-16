.PHONY: all format

all:
	pip3 install -e .

format:
	black setup.py
	black cli/*.py
	black core/*.py
	black services/*.py
	black network/*.py
	black utils/*.py