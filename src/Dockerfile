# syntax=docker/dockerfile:1
FROM debian:12-slim AS build

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -yq && apt-get install -yq --no-install-recommends \
    ca-certificates \
    curl \
    makeself

ARG ANSIBLE_RELEASE=10.0
ENV ANSIBLE_RELEASE=${ANSIBLE_RELEASE}

ARG PYTHON_RELEASE=20240814
ENV PYTHON_RELEASE=${PYTHON_RELEASE}

ARG PYTHON_VERSION=3.11.9
ENV PYTHON_VERSION=${PYTHON_VERSION}

ARG PYTHON_ARCH=x86_64
ENV PYTHON_ARCH=${PYTHON_ARCH}

WORKDIR /usr/local/src
ENV PYTHON="cpython-${PYTHON_VERSION}+${PYTHON_RELEASE}-${PYTHON_ARCH}-unknown-linux-gnu-install_only_stripped.tar.gz"
RUN curl -fsSLo "${PYTHON}" "https://github.com/indygreg/python-build-standalone/releases/download/${PYTHON_RELEASE}/${PYTHON}"
RUN tar xzf "${PYTHON}" && rm -f "${PYTHON}"

ENV PATH="/usr/local/src/python/bin:${PATH}"
RUN python -m pip install ansible~="${ANSIBLE_RELEASE}"
COPY requirements.txt .
RUN ./python3 -m pip install -r requirements.txt

FROM scratch
COPY --from=build --chown=root:root --chmod=0755 /usr/local/src/* /
