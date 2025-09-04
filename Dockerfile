# Force x86/AMD64 architecture to avoid ARM64 rollup issues on Apple Silicon
FROM --platform=linux/amd64 python:3.11.5
RUN useradd -m jupyter
RUN useradd -m user
EXPOSE 8888

# Install system dependencies
RUN apt update && apt install -y lsof rsync curl

# Install Node.js 20 and npm (required for beaker frontend builds)
RUN curl -fsSL https://nodejs.org/dist/v20.18.0/node-v20.18.0-linux-x64.tar.xz -o node.tar.xz && \
    tar -xJf node.tar.xz -C /usr/local --strip-components=1 && \
    rm node.tar.xz && \
    node --version && npm --version

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip editables debugpy uv poetry

# Install beaker-kernel from GitHub source using github's codeload API to avoid having to clone via git (slower)
ARG BEAKER_KERNEL_REF=dev
ADD https://codeload.github.com/jataware/beaker-kernel/tar.gz/$BEAKER_KERNEL_REF /tmp/beaker-kernel.tar.gz
RUN mkdir -p /tmp/beaker-kernel && \
    tar -xzf /tmp/beaker-kernel.tar.gz -C /tmp/beaker-kernel --strip-components=1

WORKDIR /tmp/beaker-kernel

# Use beaker build process
RUN make build

# Install the Python package and cleanup
# note that this is a wildcard and will match the version of the package
# that was built; it assumes the wheel is in the dist directory and there is only one
RUN uv pip install --system dist/beaker_kernel-*-py3-none-any.whl

COPY --chown=1000:1000 . /jupyter

# may or may not exist. if running locally,
# these would likely be present in project root.
# they should **NOT** be included or present in the image build.
RUN rm -f /jupyter/.beaker.conf
RUN rm -f /jupyter/.env

RUN uv pip install --system /jupyter

RUN mkdir -m 777 /var/run/beaker

WORKDIR /jupyter

# Set default server env variables
ENV BEAKER_AGENT_USER=jupyter
ENV BEAKER_SUBKERNEL_USER=user
ENV BEAKER_RUN_PATH=/var/run/beaker
ENV BEAKER_APP=biome.app.BiomeApp

# Service
CMD ["beaker", "notebook", "--ip", "0.0.0.0", "--allow-root"]