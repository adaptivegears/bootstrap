# `bootstrap` - Ansible Playbook Runner

`bootstrap` is a command-line utility that simplifies the execution of Ansible playbooks, making it easier to bootstrap systems with a consistent configuration.

## Getting Started

### Prerequisites & Installation

```shell
apt-get update && apt-get install -yq --no-install-recommends ca-certificates curl locales
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
update-locale LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8
```

```shell
curl -fsSLo /usr/local/bin/bootstrap https://github.com/adaptivegears/bootstrap/releases/download/v0.2.4/bootstrap-linux-$(uname -m)
chown root:root /usr/local/bin/bootstrap
chmod 0755 /usr/local/bin/bootstrap
```

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

## Why `bootstrap` Exists

`bootstrap` was created to solve several common challenges in system configuration and infrastructure management:

### Problem: Complex Deployment Workflows

Traditional system configuration often requires:
- Installing Python and Ansible dependencies
- Cloning repositories of playbooks and roles
- Managing inventory files and configuration
- Executing complex Ansible commands with many parameters

### Solution: Simplified System Configuration

`bootstrap` addresses these challenges by:

1. **Zero Dependencies**: The all-in-one binary includes Python and Ansible, eliminating the need to install prerequisites on target systems.

2. **Direct GitHub Integration**: Run playbooks directly from GitHub using the simple `@owner/playbook` syntax without cloning repositories.

3. **Simplified Interface**: Convert complex Ansible parameters into intuitive command-line options that make sense for each playbook.

4. **Standardized Patterns**: Encourage consistent configuration patterns across different systems and services.

5. **Observability Built-in**: OpenTelemetry integration provides visibility into deployment processes with minimal setup.

6. **CLI-First Approach**: Recognizing that Ansible blends imperative and declarative paradigms, `bootstrap` provides a CLI interface that feels more natural than trying to force a purely declarative model.

7. **Universal Compatibility**: While `bootstrap` works best with playbooks designed for it, it remains fully compatible with any standard Ansible playbook without requiring special structures or modifications.

`bootstrap` is particularly valuable for initial server setup and bootstrapping.

## License

Copyright © AdaptiveGears
