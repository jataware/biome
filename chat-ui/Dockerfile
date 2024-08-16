from beaker-kernel:latest

COPY ./beaker-biome /opt/beaker-biome
USER root
RUN chown -R jupyter:users /opt/beaker-biome
USER jupyter
RUN cd /opt/beaker-biome && hatch build
RUN pip install /opt/beaker-biome/dist/beaker_biome*.whl