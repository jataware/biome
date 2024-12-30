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

RUN pip install -e /jupyter/beaker-biome

RUN pip uninstall -y archytas

# TODO: remove this once we have a release
RUN pip install git+https://github.com/jataware/archytas.git@581a02fb5f7909ea4f763605a497ea9898b23bdf --force-reinstall --upgrade