FROM python:3.11.5
RUN useradd -m jupyter
RUN useradd -m user
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install debugpy for remote debugging
RUN pip install --upgrade --no-cache-dir hatch pip editables debugpy uv poetry

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
CMD ["python", "-m", "beaker_kernel.service.server", "--ip", "0.0.0.0"]
