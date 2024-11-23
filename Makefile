.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

ANSIBLE_ARCH ?= arm64
PYTHON_ARCH ?= aarch64
PYTHON_RELEASE ?= 20240814
PYTHON_VERSION ?= 3.11.9

.PHONY: build
build: # Build binary using Docker
	docker buildx build \
		--platform linux/$(ANSIBLE_ARCH) \
		--build-arg ANSIBLE_ARCH=$(ANSIBLE_ARCH) \
		--build-arg PYTHON_ARCH=$(PYTHON_ARCH) \
		--build-arg PYTHON_RELEASE=$(PYTHON_RELEASE) \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--progress=plain \
		--output dist src

.PHONY: run
run: build # Run shell in Docker container
	docker run -it --rm \
		-v $(shell pwd)/dist/preset-linux-$(ANSIBLE_ARCH):/usr/local/bin/preset:ro \
		-v $(shell pwd)/tests/presets:/opt/presets:ro \
		debian:12 \
		preset -- /opt/presets /opt/presets/playbooks/ping.yml
