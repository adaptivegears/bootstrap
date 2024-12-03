#!/usr/bin/env sh
set -eu

### environment ###############################################################
WORKDIR=$(CDPATH="cd -- $(dirname -- "$0")" && pwd -P)
export WORKDIR

PYTHONBIN="$WORKDIR/python/bin"
export PYTHONBIN

PATH="$PYTHONBIN:$PATH"
export PATH

### environment | python ######################################################
# ensure isolation
export PYTHONPATH="${WORKDIR}"

# ensure python3 interpreter
if $(command -v sed) --version 2>&1 | grep -q 'GNU sed'; then
    find "${PYTHONBIN}" -type f -exec sed -i '1s|^#!.*python.*$|#!/usr/bin/env '"$PYTHONBIN"'/python3|' {} \;
else
    find "${PYTHONBIN}" -type f -exec sed -i '' '1s|^#!.*python.*$|#!/usr/bin/env '"$PYTHONBIN"'/python3|' {} \;
fi

# ensure no pyc files
export PYTHONDONTWRITEBYTECODE=1

### environment | ansible #####################################################
ANSIBLE_HOME="${ANSIBLE_HOME:-$WORKDIR/.ansible}"
export ANSIBLE_HOME
mkdir -p "$ANSIBLE_HOME"

if [ -n "${ANSIBLE_ROLES_PATH:-}" ]; then
    ANSIBLE_ROLES_PATH="$ANSIBLE_HOME/roles:$ANSIBLE_ROLES_PATH"
else
    ANSIBLE_ROLES_PATH="$ANSIBLE_HOME/roles"
fi
mkdir -p "$ANSIBLE_HOME/roles"
export ANSIBLE_ROLES_PATH

if [ -n "${ANSIBLE_COLLECTIONS_PATH:-}" ]; then
    ANSIBLE_COLLECTIONS_PATH="$ANSIBLE_HOME/collections:$ANSIBLE_COLLECTIONS_PATH"
else
    ANSIBLE_COLLECTIONS_PATH="$ANSIBLE_HOME/collections"
fi
mkdir -p "$ANSIBLE_HOME/collections"
export ANSIBLE_COLLECTIONS_PATH

export ANSIBLE_OPENTELEMETRY_ENABLED=${ANSIBLE_OPENTELEMETRY_ENABLED:-false}
export ANSIBLE_OPENTELEMETRY_DISABLE_ATTRIBUTES_IN_LOGS=${ANSIBLE_OPENTELEMETRY_DISABLE_ATTRIBUTES_IN_LOGS:-false}
export ANSIBLE_OPENTELEMETRY_DISABLE_LOGS=${ANSIBLE_OPENTELEMETRY_DISABLE_LOGS:-false}
export ANSIBLE_OPENTELEMETRY_HIDE_TASK_ARGUMENTS=${ANSIBLE_OPENTELEMETRY_HIDE_TASK_ARGUMENTS:-false}

export OTEL_SERVICE_NAME=${OTEL_SERVICE_NAME:-bootstrap}
export OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT:-https://otlp.adaptivegears.studio}
export OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=${OTEL_EXPORTER_OTLP_TRACES_PROTOCOL:-grpc}

### main ######################################################################
"${PYTHONBIN}/python3" -m bootstrap "$@"
