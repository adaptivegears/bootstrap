.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

ANSIBLE_ARCH ?= arm64
PYTHON_ARCH ?= aarch64
PYTHON_RELEASE ?= 20241016
PYTHON_VERSION ?= 3.11.10

.PHONY: build
build: ## Build binary using Docker
	docker buildx build \
		--platform linux/$(ANSIBLE_ARCH) \
		--build-arg ANSIBLE_ARCH=$(ANSIBLE_ARCH) \
		--build-arg PYTHON_ARCH=$(PYTHON_ARCH) \
		--build-arg PYTHON_RELEASE=$(PYTHON_RELEASE) \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--progress=plain \
		--output dist src

.PHONY: shell
shell: build ## Run shell in Docker container
	@echo "preset -- /opt/presets /opt/presets/playbooks/ping.yml"
	@docker run -it --rm \
		-v $(shell pwd)/dist/preset-linux-$(ANSIBLE_ARCH):/usr/local/bin/preset:ro \
		-v $(shell pwd)/tests/presets:/opt/presets:ro \
		debian:12 /bin/bash

.PHONY: test
test: ## Test the binary
	@docker run --rm \
		--platform linux/$(ANSIBLE_ARCH) \
		-v $(shell pwd)/dist/preset-linux-$(ANSIBLE_ARCH):/usr/local/bin/preset:ro \
		-v $(shell pwd)/tests/presets:/opt/presets:ro \
		-v $(shell pwd)/tests/preset.bats:/usr/local/src/preset.bats:ro \
		ghcr.io/andreygubarev/bats:latest /usr/local/src

.PHONY: watch
watch: ## Watch for changes and run tests
	find . -name "*.py" | entr make test
