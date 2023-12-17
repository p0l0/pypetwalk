all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "build           -- build python package"
	@echo ""
	@echo "pypi            -- upload package to pypi"
	@echo ""
	@echo "test            -- execute test suite"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "pre-commit      -- run pre-commit tests"
	@echo ""
	@echo "pydocstyle      -- run pydocstyle tests"
	@echo ""
	@echo "coverage        -- create coverage report"
	@echo ""
	@echo "clean           -- cleanup working directory"

test:
	pytest

build:
	@python3 setup.py sdist
	@python3 setup.py egg_info

pypi:
	@rm -f dist/*
	@python setup.py sdist
	@twine upload dist/*

pylint:
	@pylint --jobs=0 pypetwalk *.py
	@pylint --jobs=0 --disable=no-self-use,protected-access,abstract-class-instantiated tests/*

pre-commit:
	@pre-commit run --all-files

pydocstyle:
	@pydocstyle pypetwalk tests/*.py tests/*.py *.py

coverage:
	pytest --cov-report html --cov pypetwalk --verbose

clean:
	-rm -rf build dist pypetwalk.egg-info
	-rm -rf .tox
	-rm -rf .coverage htmlcov

.PHONY: test build clean
