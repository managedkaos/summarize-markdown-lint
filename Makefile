APP = $(notdir $(CURDIR))
TAG = $(shell echo "$$(date +%F)-$$(git rev-parse --short HEAD)")
DOCKER_REPO = ghcr.io/managedkaos


help: ## Display available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

requirements: ## Install Python dependencies
	pip install --upgrade pip
	pip install --quiet --upgrade --requirement requirements.txt

lint: ## Run static checks
	flake8 --ignore=E501,E231 *.py
	pylint --errors-only --disable=C0301 *.py
	black --diff *.py

black: ## Format Python files
	black *.py

test: ## Run the test suite
	python -m unittest discover --verbose --failfast -s tests

build: pip lint ## Build the Docker image
	docker build --tag $(APP):$(TAG) .

docker-test: requirements test build ## Run tests, build image, and check sample input
	cat tests/sample.txt | docker run --interactive $(APP):$(TAG)

clean: ## Remove containers and caches
	docker container stop $(APP) || true
	docker container rm $(APP) || true
	@rm -rf ./__pycache__ ./tests/__pycache__
	@rm -f .*~ *.pyc

.PHONY: build clean deploy help interactive lint pip run test unittest upload
