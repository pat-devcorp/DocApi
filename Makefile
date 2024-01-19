# Makefile for python code
# 
# > make help
#
# The following commands can be used.
#
# init:  sets up environment and installs requirements
# lint:  Runs flake8 on src, exit if critical rules are broken
# clean:  Remove build and cache files
# test:  Run pytest
# run:  Executes the logic

VENV_PATH = .venv/bin/activate
ENVIRONMENT_VARIABLE_FILE = .env
DOCKER_NAME ?= my-docker-name
DOCKER_TAG ?= latest

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

define export.functions
	@unset $(grep -v '^#' $(ENVIRONMENT_VARIABLE_FILE) | sed -E 's/(.*)=.*/\1/' | xargs)
	@export $(cat $(ENVIRONMENT_VARIABLE_FILE) | xargs) 
	@printenv
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

# Load environment variables from the defined .env file
include $(ENVIRONMENT_VARIABLE_FILE)

export-env: ## export environment variables
export-env:
	$(call export.functions)
	
init: ## sets up environment and installs requirements
init:
	pip install -r /init/requirements.txt
	# Used for packaging and publishing
	pip install setuptools wheel twine
	# Used for linting and formatting
	pip install flake8
	pip install autoflake
	pip install black
	pip install isort
	pip install pydocstyle
	# Used for testing
	pip install pytest

lint: ## Runs flake8 on src, exit if critical rules are broken
lint:
	# order imports
	isort .
	# format code
	black .
	# stop the build if there are Python syntax errors or undefined names
	flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 src --count --exit-zero --statistics --ignore=E501

clean: ## Remove build and cache files
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .pytest_cache
	# Remove all pycache
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

test: ## Run pytest
test:
	pytest tests -s

build: ## Build docker image
build:
	sed -i 's/\r/\n/g' ./init/entrypoint.sh
	@docker image rm -f $(DOCKER_NAME):$(API_VERSION) || true
	docker build -t $(DOCKER_NAME):$(API_VERSION) --file Dockerfile.prod .

run: ## Run docker container
run:
	@if [ -n "$$(docker ps -a -q -f name=$(DOCKER_NAME))" ]; then \
        docker rm -f $(DOCKER_NAME); \
    fi
	docker run -p 5000:$(API_PORT) --name $(DOCKER_NAME) $(DOCKER_NAME):$(API_VERSION)

dev: ##Run with docker-compose 
dev:
	docker-compose up -d

logs: ## Show container logs
logs:
	docker logs -f $(DOCKER_NAME)