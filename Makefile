MAKEFLAGS     = --no-print-directory --no-builtin-rules
.DEFAULT_GOAL = all

# Variables
USER:=
PACKAGE:=skeleton

# If virtualenv exists, use it. If not, use PATH to find
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYTHON         = venv/bin/python

all: venv install

.PHONY: all

## Environment

venv: venv/deps

venv/deps: requirements.txt
	test -d venv || $(SYSTEM_PYTHON) -m venv venv
	. venv/bin/activate
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade pip -r requirements.txt
	touch venv/deps

venv/test_deps: venv/deps requirements_test.txt
	test -d venv || $(SYSTEM_PYTHON) -m venv venv
	. venv/bin/activate
	$(PYTHON) -m pip install --upgrade pip -r requirements_test.txt
	touch venv/test_deps

.PHONY: install

## install

install: venv
	$(PYTHON) -m pip install --use-pep517 --prefix=venv .

.PHONY: install

## DB

db: venv
	rm db/config.db || true
	$(PYTHON) -m alembic upgrade head

.PHONY: db

test_db: venv
	rm db/test_*.db || true
	$(PYTHON) -m alembic --name test upgrade head

.PHONY: test_db

## Lint, test

test: venv/test_deps
	$(PYTHON) -m pytest tests

lint: venv/test_deps
	@( echo Flake8 )
	$(PYTHON) -m flake8 $(PACKAGE) || true
	@( echo;echo PyDocStyle)
	$(PYTHON) -m pydocstyle $(PACKAGE) || true
	@( echo;echo Black )
	$(PYTHON) -m black --check $(PACKAGE) tests setup.py

lintfix: venv/test_deps
	@( echo;echo Black )
	$(PYTHON) -m black $(PACKAGE) tests setup.py
	@( echo;echo iSort )
	$(PYTHON) -m isort --atomic $(PACKAGE)

.PHONY: test lint lintfix

## Clean
clean:
	$(PYTHON) -m pip uninstall $(PACKAGE) -y || true
	python setup.py clean --all
	rm -rf *.egg-info build dist tests/reports docs/build .pytest_cache .tox .coverage html/ db/test.db
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean_venv: clean
	rm -rf venv

.PHONY: clean clean_venv
