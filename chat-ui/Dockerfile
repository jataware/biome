FROM python:3.10
RUN useradd -m jupyter
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip beaker-kernel debugpy

USER jupyter
WORKDIR /jupyter

COPY ./beaker-biome /jupyter/beaker-biome
COPY ./beaker_kernel-1.7.4a1-py3-none-any.whl /tmp/
USER root
RUN chown -R jupyter:users /jupyter/beaker-biome

USER jupyter
RUN pip install /tmp/beaker_kernel-1.7.4a1-py3-none-any.whl
RUN pip install -e /jupyter/beaker-biome