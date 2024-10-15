FROM python:3.10
RUN useradd -m jupyter
EXPOSE 8888

RUN apt update && apt install -y lsof
RUN pip install --upgrade --no-cache-dir hatch pip beaker-kernel

USER jupyter
WORKDIR /jupyter

COPY ./beaker-biome /jupyter/beaker-biome
USER root
RUN chown -R jupyter:users /jupyter/beaker-biome

COPY ./beaker_kernel-1.6.8-py3-none-any.whl /jupyter/beaker_kernel-1.6.8-py3-none-any.whl
RUN chown -R jupyter:jupyter /jupyter/beaker_kernel-1.6.8-py3-none-any.whl
USER jupyter
RUN pip install /jupyter/beaker_kernel-1.6.8-py3-none-any.whl

# RUN cd /opt/beaker-biome && hatch build
# RUN pip install /opt/beaker-biome/dist/beaker_biome*.whl
RUN pip install -e /jupyter/beaker-biome
