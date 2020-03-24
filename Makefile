.DEFAULT_GOAL := help
VERSION := $(shell echo `grep __version__ robots/__init__.py | cut -d '"' -f 2`)

check:
	python -m twine check dist/*

clean:
	find . -name '*.pyc' -delete || true
	find . -name '__pycache__' -type d | xargs rm -rf || true
	find . -name '.pytest_cache' -type d | xargs rm -rf || true
	rm *.bak || true
	rm -rf .cache build dist robotspy.egg-info || true

deploy:
	python -m twine upload dist/*

dist: version test clean wheel check

fmt:
	black robots

freeze:
	pip freeze | grep -v robotspy > requirements.txt

help:
	@echo 'Makefile for RobotsPy (Python robots.txt parser)'
	@echo
	@echo 'Usage:'
	@echo '    make check      Check the wheel'
	@echo '    make clean      Delete temp files (*.pyc), caches (__pycache__)'
	@echo '    make deploy     Deploy package to the Cheese Shop (PyPI)'
	@echo '    make dist       Clean, generate the distribution and check'
	@echo '    make fmt        Format Python files using Black (Assuming Black installed globally)'
	@echo '    make freeze     Update the requirements.txt excluding local package (robotspy)'
	@echo '    make help       Display this help message'
	@echo '    make lint       Lint Python file using Pylint (Assuming Pylint installed globally)'
	@echo '    make test       Execute tests'
	@echo '    make tree       Display the dependency tree (using pipdeptree)'
	@echo '    make type       Type checking using Mypy (assuming Mypy installed globally)'
	@echo '    make version    Display current package version'
	@echo '    make wheel      Build the wheel'

lint:
	pylint robots

tag:
	git push
	git tag -a ${VERSION} -m 'Version ${TAG}'
	git push --tags

test:
	pytest tests -vv

tree:
	pipdeptree

type:
	mypy robots

version:
	@echo 'robots version: ${VERSION}'
	@perl -pi.bak -e 's/version="(\d+\.\d+\.\d+.*)"/version="${VERSION}"/' setup.py

wheel:
	python setup.py sdist bdist_wheel

.PHONY: check clean deploy dist fmt help lint test type version wheel
