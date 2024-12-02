# syntax=docker/dockerfile:1
FROM debian:12 AS build

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -yq && apt-get install -yq --no-install-recommends \
    ca-certificates \
    curl \
    makeself

ARG PACKAGE_ARCH=x86_64
ENV PACKAGE_ARCH=${PACKAGE_ARCH}

ARG PYTHON_RELEASE=20241016
ENV PYTHON_RELEASE=${PYTHON_RELEASE}

ARG PYTHON_VERSION=3.11.10
ENV PYTHON_VERSION=${PYTHON_VERSION}

WORKDIR /usr/local/src
ENV PYTHON="cpython-${PYTHON_VERSION}+${PYTHON_RELEASE}-${PACKAGE_ARCH}-unknown-linux-gnu-install_only_stripped.tar.gz"
RUN curl -fsSLo "${PYTHON}" "https://github.com/indygreg/python-build-standalone/releases/download/${PYTHON_RELEASE}/${PYTHON}"
RUN tar xzf "${PYTHON}" && rm -f "${PYTHON}"

ENV PYTHONBIN="/usr/local/src/python/bin"
ENV PATH="${PYTHONBIN}:${PATH}"
COPY requirements.txt python
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install -r python/requirements.txt
RUN find "${PYTHONBIN}" -type f -exec sed -i '1s|^#!.*python.*$|#!/usr/bin/env python3|' {} \;
RUN rm -r python/share
RUN find python -type d -name "__pycache__" -print | xargs rm -rf
RUN find python -type d -name "tests" -print | xargs rm -rf

COPY --chmod=0755 --chown=root:root entrypoint.sh .
COPY bootstrap bootstrap
RUN makeself --header "/usr/share/makeself/makeself-header.sh" \
    --gzip --complevel 1 \
    --nomd5 --nocrc \
    --tar-format gnu \
    --tar-quietly \
    --tar-extra '--mtime=2024-01-01' \
    --packaging-date '2024-01-01T00:00:00Z' \
    "/usr/local/src" \
    "/usr/local/bin/bootstrap-linux-${PACKAGE_ARCH}" \
    "bootstrap (Python ${PYTHON_VERSION})" \
    ./entrypoint.sh

FROM scratch
ARG PACKAGE_ARCH=x86_64
ENV PACKAGE_ARCH=${PACKAGE_ARCH}
COPY --from=build --chown=root:root --chmod=0755 "/usr/local/bin/bootstrap-linux-${PACKAGE_ARCH}" /
