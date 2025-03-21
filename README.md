# Bootstrap - Ansible Playbook Runner

Bootstrap is a command-line utility that simplifies the execution of Ansible playbooks, making it easier to bootstrap systems with a consistent configuration.

## Features

- Run Ansible playbooks from local collections or directly from GitHub
- Simplified command-line interface
- Built-in Python interpreter (no external dependencies)
- OpenTelemetry support for monitoring and observability

## Installation

```shell
curl -fsSLo /usr/local/bin/bootstrap https://github.com/adaptivegears/bootstrap/releases/download/v0.2.4/bootstrap-linux-$(uname -m)
chmod +x /usr/local/bin/bootstrap
```

## Usage

### Run a playbook from GitHub

```shell
bootstrap @<owner>/<playbook>[/<reference>] [extra_vars]
```

Examples:
```shell
# Run the standard-debian playbook from adaptivegears
bootstrap @adaptivegears/standard-debian --prune

# Run the standard-ssh playbook with a specific user
bootstrap @adaptivegears/standard-ssh -U andreygubarev

# Run a specific version of a playbook
bootstrap @adaptivegears/ping/v1.0.0
```

## Environment Variables

The following environment variables can be used to configure OpenTelemetry:

- `ANSIBLE_OPENTELEMETRY_ENABLED`: Enable OpenTelemetry (default: false)
- `OTEL_SERVICE_NAME`: Service name (default: bootstrap)
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP endpoint (default: https://otlp.adaptivegears.studio)
- `OTEL_EXPORTER_OTLP_PROTOCOL`: OTLP protocol (default: grpc)

## Building from Source

The project uses a Makefile for building and testing. Here are the main commands:

```shell
# Build the bootstrap binary
make build

# Run tests
make test

# Run a shell with bootstrap available
make shell

# Run the bootstrap command directly
make run

# Watch for changes and automatically rebuild and run
make watch
```

You can customize the build with the following variables:

```shell
# Example: Build for a different architecture
make build PLATFORM_OS=linux PLATFORM_ARCH=amd64 PACKAGE_ARCH=x86_64

# Example: Use a specific Python version
make build PYTHON_VERSION=3.12.0 PYTHON_RELEASE=20240205
```

Available configuration variables:
- `PLATFORM_OS`: Target OS (default: linux)
- `PLATFORM_ARCH`: Docker platform architecture (default: arm64)
- `PACKAGE_ARCH`: Python package architecture (default: aarch64)
- `PYTHON_RELEASE`: Python build release date (default: 20250317)
- `PYTHON_VERSION`: Python version (default: 3.11.11)

The built binary will be in the `dist` directory.

## License

Copyright © AdaptiveGears
