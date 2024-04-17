FROM python:3.10
RUN useradd -m jupyter
EXPOSE 8888

RUN apt update && apt install -y lsof

# Install Python requirements
RUN pip install --upgrade --no-cache-dir hatch pip

USER jupyter

RUN pip install beaker_kernel
WORKDIR /home/jupyter/workdir

CMD ["python", "-m", "beaker_kernel.server.main", "--ip", "0.0.0.0"]
