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
unset PYTHONPATH

# ensure python3 interpreter
if $(command -v sed) --version 2>&1 | grep -q 'GNU sed'; then
    find "${PYTHONBIN}" -type f -exec sed -i '1s|^#!.*python.*$|#!/usr/bin/env '"$PYTHONBIN"'/python3|' {} \;
else
    find "${PYTHONBIN}" -type f -exec sed -i '' '1s|^#!.*python.*$|#!/usr/bin/env '"$PYTHONBIN"'/python3|' {} \;
fi

# ensure no pyc files
export PYTHONDONTWRITEBYTECODE=1
