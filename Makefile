.DEFAULT_GOAL := help
PROJECT := robotspy
VERSION := $(shell echo `grep __version__ robots/__init__.py | cut -d '"' -f 2`)

# twine installed globally
check:
	twine check dist/*

clean:
	find . -name '*.pyc' -delete || true
	find . -name '__pycache__' -type d | xargs rm -rf || true
	find . -name '.pytest_cache' -type d | xargs rm -rf || true
	rm *.bak || true
	rm -rf .cache build dist robotspy.egg-info || true

# twine installed globally
deploy:
	twine upload dist/*

difflib: SHELL:=/bin/bash
difflib:
	diff -w <(pip freeze) <(cat requirements.txt)


dist: freeze version test clean wheel check

docker:
	docker build -t 'andreburgaud/${PROJECT}:${VERSION}' .

docker-scout: docker
	docker scout cves 'andreburgaud/${PROJECT}:${VERSION}'

docker-deploy: docker-scout
	docker push 'docker.io/andreburgaud/${PROJECT}:${VERSION}'
	docker tag 'andreburgaud/${PROJECT}:${VERSION}' 'docker.io/andreburgaud/${PROJECT}:latest'
	docker push 'docker.io/andreburgaud/${PROJECT}:latest'

# black installed globally
fmt:
	black robots

freeze:
	pip-chill | grep -v robotspy > requirements.txt

help:
	@echo 'Makefile for RobotsPy (Python robots.txt parser)'
	@echo
	@echo 'Usage:'
	@echo '    make check         Check the wheel'
	@echo '    make clean         Delete temp files (*.pyc), caches (__pycache__)'
	@echo '    make deploy        Deploy package to the Cheese Shop (PyPI)'
	@echo '    make difflib       Identify differences between libraries installed and requirement.txt file'
	@echo '    make dist          Clean, generate the distribution and check'
	@echo '    make docker        Build a docker image using the Dockerfile at the root of hte repo'
	@echo '    make docker-scout  Validate the image against CVEs (requires docker scout to be installed on the build system)'
	@echo '    make docker-deploy Push the docker image to Docker Hub (requires a docker hub account)'
	@echo '    make fmt           Format Python files using Black (installed globally)'
	@echo '    make freeze        Update the requirements.txt excluding local package (robotspy)'
	@echo '    make help          Display this help message'
	@echo '    make lint          Lint Python file using Pylint (installed globally)'
	@echo '    make test          Execute tests'
	@echo '    make type          Type checking using Mypy (installed globally)'
	@echo '    make version       Display current package version'
	@echo '    make wheel         Build the wheel'

# pylint installed globally
lint:
	pylint robots

tag:
	git push
	git tag -a ${VERSION} -m 'Version ${TAG}'
	git push --tags

test:
	pytest tests -vv

# mypy installed globally
type:
	mypy --check-untyped-defs robots

version:
	@echo 'robots version: ${VERSION}'
	@perl -pi.bak -e 's/version="(\d+\.\d+\.\d+.*)"/version="${VERSION}"/' setup.py

wheel:
	python setup.py sdist bdist_wheel
