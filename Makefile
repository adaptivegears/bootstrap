.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


PLATFORM_OS ?= linux
PLATFORM_ARCH ?= arm64
PACKAGE_ARCH ?= aarch64

PYTHON_RELEASE ?= 20241016
PYTHON_VERSION ?= 3.11.10

.PHONY: build
build: ## Build binary using Docker
	docker buildx build \
		--platform $(PLATFORM_OS)/$(PLATFORM_ARCH) \
		--build-arg PACKAGE_ARCH=$(PACKAGE_ARCH) \
		--build-arg PYTHON_RELEASE=$(PYTHON_RELEASE) \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--progress=plain \
		--output dist src
	chmod +x $(shell pwd)/dist/bootstrap-$(PLATFORM_OS)-$(PACKAGE_ARCH)

.PHONY: shell
shell: build ## Run shell in Docker container
	@echo "bootstrap -- /opt/collection /opt/collection/playbooks/ping.yml"
	@docker run -it --rm \
		--platform $(PLATFORM_OS)/$(PLATFORM_ARCH) \
		-v $(shell pwd)/dist/bootstrap-linux-$(PACKAGE_ARCH):/usr/local/bin/bootstrap:ro \
		-v $(shell pwd)/tests/collection:/opt/collection:ro \
		debian:12 /bin/bash

.PHONY: run
run: build ## Run shell in Docker container
	@docker run -it --rm \
		--platform $(PLATFORM_OS)/$(PLATFORM_ARCH) \
		-v $(shell pwd)/dist/bootstrap-linux-$(PACKAGE_ARCH):/usr/local/bin/bootstrap:ro \
		-v $(shell pwd)/tests/collection:/opt/collection:ro \
		debian:12 /bin/bash -c 'bootstrap -- /opt/collection /opt/collection/playbooks/ping.yml'

.PHONY: test
test: ## Test the binary
	@chmod +x $(shell pwd)/dist/bootstrap-linux-$(PACKAGE_ARCH)
	@docker run --rm \
    	--platform $(PLATFORM_OS)/$(PLATFORM_ARCH) \
		-v $(shell pwd)/dist/bootstrap-linux-$(PACKAGE_ARCH):/usr/local/bin/bootstrap:ro \
		-v $(shell pwd)/tests/collection:/opt/collection:ro \
		-v $(shell pwd)/tests/bootstrap.bats:/usr/local/src/bootstrap.bats:ro \
		ghcr.io/andreygubarev/bats:latest /usr/local/src

.PHONY: watch
watch: ## Watch for changes and run tests
	find . -name "*.py" | entr make run
