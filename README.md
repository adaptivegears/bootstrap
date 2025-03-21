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

Bootstrap provides a simple way to run Ansible playbooks, especially those designed for system configuration.

### Basic Usage

```shell
# Run a playbook from GitHub using the @ syntax
bootstrap @owner/playbook [options]

# Run a local playbook
bootstrap /path/to/playbook.yml [options]
```

### GitHub Playbook References

The GitHub playbook reference format is:

```
@owner/repository[/reference]
```

Where:
- `owner`: GitHub organization or username
- `repository`: Repository name (typically matches the playbook name)
- `reference` (optional): Branch, tag, or commit hash (defaults to main)

### Common Options

Many playbooks support standard options:

- `-h, --help`: Show help message for the playbook
- `-i, --install`: Install the specified software/service
- Various other options depending on the playbook

### Examples

```shell
# Basic playbook execution
bootstrap @adaptivegears/standard-debian

# Run with options
bootstrap @adaptivegears/standard-debian --prune

# SSH configuration with GitHub user authorization
bootstrap @adaptivegears/standard-ssh -U andreygubarev

# Run a specific version of a playbook
bootstrap @adaptivegears/ping/v1.0.0

# Configure Tailscale with an auth token
bootstrap @adaptivegears/tailscale --token tskey-1234567890

# View help for a playbook
bootstrap @adaptivegears/standard-kubernetes --help

# Pass multiple options
bootstrap @adaptivegears/standard-debian --minimal --prune --hostname=webserver
```

### Working with Elevated Privileges

Some playbooks require root privileges:

```shell
# Run with sudo
sudo bootstrap @adaptivegears/standard-debian

# Or use sudo -E to preserve environment variables
sudo -E bootstrap @adaptivegears/standard-debian
```

### Using Environment Variables

Many playbooks support configuration via environment variables:

```shell
# Set variables before running
export DEBIAN_HOSTNAME=webserver
export DEBIAN_TOPOLOGY_REGION=us-west
bootstrap @adaptivegears/standard-debian

# Or set inline
DEBIAN_PRUNE=true bootstrap @adaptivegears/standard-debian
```

### Common Playbooks

| Playbook | Description | Common Options |
|----------|-------------|----------------|
| `@adaptivegears/standard-debian` | Configure Debian system | `--prune`, `--minimal`, `--hostname` |
| `@adaptivegears/standard-ssh` | Configure SSH access | `-U <github-user>`, `--enable-hardening` |
| `@adaptivegears/standard-kubernetes` | Install Kubernetes components | Varies by component |
| `@adaptivegears/standard-tailscale` | Configure Tailscale VPN | `--token`, `--advertise-exit-node` |

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
