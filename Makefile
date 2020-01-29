.DEFAULT_GOAL := help

check:
	python -m twine check dist/*

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -rf
	find . -name '.pytest_cache' -type d | xargs rm -rf
	rm -rf .cache build dist robotspy.egg-info

deploy:
	python -m twine upload dist/*

dist: clean wheel check

fmt:
	black robots

help:
	@echo 'Makefile for RobotsPy (Python robots.txt parser)'
	@echo
	@echo 'Usage:'
	@echo '    make check      Check the wheel'
	@echo '    make clean      Delete temp files (*.pyc), caches (__pycache__)'
	@echo '    make deploy     Deploy package to the Cheese Shop (PyPI)'
	@echo '    make dist       Clean, generate the distribution and check'
	@echo '    make fmt        Format Python files using Black (Assuming Black installed globally)'
	@echo '    make help       Display this help message'
	@echo '    make lint       Lint Python file using Pylint (Assuming Pylint installed globally)'
	@echo '    make test       Execute tests'
	@echo '    make type       Type checking using Mypy (assuming Mypy installed globally)'
	@echo '    make wheel      Build the wheel'

lint:
	pylint robots

test:
	pytest tests -vv

type:
	mypy robots

wheel:
	python setup.py sdist bdist_wheel

.PHONY: check clean deploy dist fmt help lint test type wheel
