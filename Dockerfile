FROM python:3.11.5
RUN useradd -m jupyter
RUN useradd -m user
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip editables debugpy

# Install beaker-kernel from dev branch
# RUN pip install git+https://github.com/jataware/beaker-kernel.git@dev
COPY --chown=1000:1000 . /jupyter
RUN chown -R 1000:1000 /jupyter

RUN pip install \
    beaker-kernel~=1.9.1 \
    archytas==1.3.11 \
    requests \
    google-generativeai \
    PyYAML \
    adhoc-api~=1.0.0 \
    idc-index \
    seaborn \
    biopython \
    boto3 \
    google-cloud-storage \
    PyPDF2~=3.0.1

RUN pip install --no-build-isolation -e /jupyter

RUN mkdir -m 777 /var/run/beaker

WORKDIR /jupyter

# Set default server env variables
ENV BEAKER_AGENT_USER=jupyter
ENV BEAKER_SUBKERNEL_USER=user
ENV BEAKER_RUN_PATH=/var/run/beaker
ENV BEAKER_APP=biome.app.BiomeApp

#ENV CONFIG_TYPE=session

# Service
CMD ["python", "-m", "beaker_kernel.service.server", "--ip", "0.0.0.0"]
