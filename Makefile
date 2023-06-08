.DEFAULT_GOAL := help
.PHONY: all

PROJECT_NAME=$(shell grep "name" pyproject.toml | cut -d "\"" -f 2)

help:
	@# Got it from here: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

deps: ## Installs project dependencies
	poetry install --no-root

deps-outdated: ## Shows outdated dependencies
	poetry show --outdated

clean: ## Resets the development environment to the initial state
	-find . -name "*.pyc" -delete
	-rm requirements.txt
	-rm dist/${PROJECT_NAME}*
	-poetry env remove --quiet --all

setup: deps ## Sets up the developement environment
	poetry run pre-commit install

check: ## Runs static checks on the code
	poetry run pre-commit run --all

unit-tests: ## Runs the unit tests
	poetry run pytest ./src  -svv -m "not integration" -n 4

integration-tests: ## Runs the integration tests
	# poetry run pytest ./src  -svv -m "integration"

acceptance-tests: ## Runs the acceptance tests
	# poetry run pytest ./features  -svv
	
tests: unit-tests integration-tests acceptance-tests  ## Runs all the tests

coverage: ## Shows coverage in the browser
	poetry run coverage run -m pytest .
	poetry run coverage html
	open htmlcov/index.html

future: ## Tests the code against multiple python versions
	poetry export -f requirements.txt --output requirements.txt --with dev
	poetry run nox
	-rm requirements.txt

build:  ## Builds this project into a package
	poetry install	# This is needed to update the version in pyproject.toml
	poetry run python -m toolcat.project update_version_in_pyproject_toml $(shell poetry version patch)
	poetry build

publish: setup check tests build ## Publish the package to the PyPi
	$(eval VERSION=$(shell grep name -A 1 pyproject.toml | grep "version" | cut -d "\"" -f 2))
	git commit -a -m "Release version $(VERSION)"
	poetry publish --build
	git push origin main

all: clean setup check tests future