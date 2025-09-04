# Force x86/AMD64 architecture to avoid ARM64 rollup issues on Apple Silicon
FROM --platform=linux/amd64 python:3.11.5

# Create users early (rarely changes)
RUN useradd -m jupyter && useradd -m user
EXPOSE 8888

# Install system dependencies (rarely changes)
RUN apt update && apt install -y lsof rsync curl wget

# Install Node.js 20 and npm (rarely changes)
RUN curl -fsSL https://nodejs.org/dist/v20.18.0/node-v20.18.0-linux-x64.tar.xz -o node.tar.xz && \
    tar -xJf node.tar.xz -C /usr/local --strip-components=1 && \
    rm node.tar.xz && \
    node --version && npm --version

# Install Python build tools (rarely changes)
RUN pip install --upgrade --no-cache-dir hatch pip editables debugpy uv poetry

# Download ChEMBL database EARLY (huge file, rarely changes)
ARG DOWNLOAD_CHEMBL_DATABASE=false
RUN if [ "$DOWNLOAD_CHEMBL_DATABASE" = "true" ]; then \
        mkdir -p /jupyter && \
        echo "Downloading and extracting ChEMBL database (several GB, this may take a while)..." && \
        wget --progress=dot:giga https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_35_sqlite.tar.gz -O- | tar -xzf - -C /jupyter && \
        echo "ChEMBL database ready at /jupyter/chembl_35/"; \
    fi

# Install archytas from GitHub source (changes when you update REF)
ARG ARCHYTAS_REF=main
ADD https://codeload.github.com/jataware/archytas/tar.gz/$ARCHYTAS_REF /tmp/archytas.tar.gz
RUN mkdir -p /tmp/archytas && \
    tar -xzf /tmp/archytas.tar.gz -C /tmp/archytas --strip-components=1
WORKDIR /tmp/archytas
RUN uv pip install --system .

# Install beaker-kernel from GitHub source (changes when you update REF)
ARG BEAKER_KERNEL_REF=dev
ADD https://codeload.github.com/jataware/beaker-kernel/tar.gz/$BEAKER_KERNEL_REF /tmp/beaker-kernel.tar.gz
RUN mkdir -p /tmp/beaker-kernel && \
    tar -xzf /tmp/beaker-kernel.tar.gz -C /tmp/beaker-kernel --strip-components=1

WORKDIR /tmp/beaker-kernel
RUN make build && \
    uv pip install --system dist/beaker_kernel-*-py3-none-any.whl

# Copy source code and install
COPY --chown=1000:1000 . /jupyter
WORKDIR /jupyter

# Clean up sensitive files and install local package
RUN rm -f /jupyter/.beaker.conf /jupyter/.env && \
    uv pip install --system /jupyter

# Create runtime directories
RUN mkdir -m 777 /var/run/beaker

# Set jupyter user's HOME to point to /jupyter
# This is a workaround for the fact that the jupyter user is created with the home directory /home/jupyter
# which is not sync'd to the /jupyter directory (which is shown in the UI as the home directory)
RUN usermod -d /jupyter jupyter

# Set default server env variables
ENV BEAKER_AGENT_USER=jupyter \
    BEAKER_SUBKERNEL_USER=jupyter \
    BEAKER_RUN_PATH=/var/run/beaker \
    BEAKER_APP=biome.app.BiomeApp

# Service
CMD ["python", "-m", "beaker_kernel.service.server", "--ip", "0.0.0.0"]