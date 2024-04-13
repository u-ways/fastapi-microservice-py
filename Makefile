################################################################################################
# FastAPI Microservice (Py) Makefile
#
# This Makefile is split into three sections:
#   - Application: for building, testing, and publishing the project.
#   - Development: for formatting, linting, and other development tasks.
#   - Docker: for building, running, and publishing Docker images.
#
# We write our rule names in the following format: [verb]-[noun]-[noun], e.g. "build-app".
#
# Variables ####################################################################################

APP_VERSION?=DEV-SNAPSHOT
APP_NAME?=fastapi-microservice-py

IMAGE_ID?=$(APP_NAME):$(APP_VERSION)
IMAGE_SAVE_LOCATION?=./build/images
OPENAPI_SAVE_LOCATION?=./build/openapi

# Application ##################################################################################

clean-app: require-poetry
	@echo "Cleaning application..."
	@poetry run pyclean -v .

build-app: require-poetry
	@echo "Building application..."
	@poetry install

test-app: install-dependencies
	@echo "Testing application..."
	poetry run pytest -v

run-app: build-app
	@echo "Running application..."
	@poetry run uvicorn src.main:app --app-dir ./src --host localhost --port 8000 --reload

# Development ##################################################################################

require-poetry:
	@echo "Checking for Poetry..."
	@command -v poetry >/dev/null 2>&1 || (echo "Poetry is required. Please install via 'make install-poetry'." && exit 1)

install-poetry:
	@echo "Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | python3 -

install-dependencies: require-poetry
	@echo "Installing dependencies..."
	@poetry install --compile --no-root

update-dependencies: require-poetry
	@echo "Updating dependencies..."
	@poetry update

lock-dependencies: require-poetry
	@echo "Locking dependencies..."
	@poetry lock

format-code: require-poetry
	@echo "Formatting application..."
	@poetry run black .

lint-code: require-poetry
	@echo "Linting application..."
	@poetry run flake8 .

check-format: require-poetry
	@echo "Checking application formatting..."
	@poetry run black --check .

check-lint: require-poetry
	@echo "Checking application linting..."
	@poetry run flake8 --show-source --statistics --count .

make check-code-quality: check-format check-lint

# Docker #######################################################################################

require-docker:
	@echo "Checking for Docker..."
	@command -v docker >/dev/null 2>&1 || (echo "Docker is required. Please install via 'make install-docker'." && exit 1)

test-app-docker: require-docker
	@echo "Testing application... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,pytest -v)

check-format-docker: require-docker
	@echo "Checking application formatting... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,black --check .)

check-lint-docker: require-docker
	@echo "Checking application linting... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,flake8 --show-source --statistics --count --max-line-length=120 .)

run-app-docker-dev: require-docker
	@docker stop fastapi-dev || true
	@echo "Running application in development mode... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,,-d -p 8000:8000)

run-app-docker-prod: require-docker
	@echo "Running application in production mode... (Containerised)"
	@$(call build_docker_image,production)
	@docker run -p 80:80 --name fastapi-prod --rm $(IMAGE_ID)

export-production-image: require-docker
	@echo "Exporting Docker image..."
	@$(call build_docker_image,production)
	@mkdir -p $(IMAGE_SAVE_LOCATION)
	@docker save -o $(IMAGE_SAVE_LOCATION)/$(APP_NAME)-$(APP_VERSION).tar $(IMAGE_ID)

export-openapi-schema: run-app-docker-dev
	@echo "Exporting OpenAPI schema..."
	@mkdir -p $(OPENAPI_SAVE_LOCATION)
	@sleep 5
	@curl -s http://0.0.0.0:8000/openapi.json > $(OPENAPI_SAVE_LOCATION)/openapi.json
	@docker stop fastapi-dev || true
	@docker run --rm -v $(OPENAPI_SAVE_LOCATION):/build redocly/cli build-docs --api=/build/openapi.json --output=/build/index.html

# Functions ####################################################################################

define build_docker_image
	@echo "Building Docker image for target: $(1)"
	@docker build --target $(1) --build-arg APP_VERSION=$(APP_VERSION) --build-arg APP_NAME=$(APP_NAME) -t $(IMAGE_ID) .
endef

define run_docker_dev_mount
	@docker run $(2) \
		-v $(PWD)/src:/app/src \
		-v $(PWD)/tests:/app/tests \
		-v $(PWD)/.env:/app/.env \
		--rm --name fastapi-dev $(IMAGE_ID) $(1)
endef
