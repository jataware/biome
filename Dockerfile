FROM python:3.11.5
RUN useradd -m jupyter
RUN useradd -m user
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip editables debugpy uv

COPY --chown=1000:1000 . /jupyter

# may or may not exist. if running locally,
# these would likely be present in project root.
# they should **NOT** be included or present in the image build.
RUN rm -f /jupyter/.beaker.conf
RUN rm -f /jupyter/.env

RUN uv pip install --system -v -e /jupyter

RUN uv pip install --system --no-deps --upgrade /jupyter/beaker_kernel-1.11.2-py3-none-any.whl

RUN mkdir -m 777 /var/run/beaker

WORKDIR /jupyter

# Set default server env variables
ENV BEAKER_AGENT_USER=jupyter
ENV BEAKER_SUBKERNEL_USER=user
ENV BEAKER_RUN_PATH=/var/run/beaker
ENV BEAKER_APP=biome.app.BiomeApp

RUN ln -s /jupyter/src/biome/datasources /home/user/datasources
# subkernel access / file pane
RUN ln -s /jupyter/data /home/user/data
# agent path resolution
RUN ln -s /jupyter/data /home/jupyter/data

RUN pip install --no-deps --upgrade "docstring-parser>=0.16"
RUN pip install "paper-qa~=5.21.0"


# Service
CMD ["python", "-m", "beaker_kernel.service.server", "--ip", "0.0.0.0"]
