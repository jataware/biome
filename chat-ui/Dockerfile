FROM python:3.10
RUN useradd -m jupyter
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip beaker-kernel debugpy

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip beaker-kernel debugpy

USER jupyter
WORKDIR /jupyter

COPY ./beaker-biome /jupyter/beaker-biome
USER root
RUN chown -R jupyter:users /jupyter/beaker-biome

USER jupyter

# TODO: remove this once we have a release
RUN pip install git+https://github.com/jataware/archytas.git@3619d3d99be001fbfaefa173389ee720e57070ce --force-reinstall --upgrade

RUN pip install -e /jupyter/beaker-biome
