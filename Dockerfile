FROM python:3.10
RUN useradd -m jupyter
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip debugpy

# Install beaker-kernel from dev branch
# RUN pip install git+https://github.com/jataware/beaker-kernel.git@dev
RUN pip install beaker-kernel==1.8.12

USER jupyter
WORKDIR /jupyter

COPY ./src/beaker-biome /jupyter/beaker-biome
USER root
RUN chown -R jupyter:users /jupyter/beaker-biome

USER jupyter

RUN pip install -e /jupyter/beaker-biome