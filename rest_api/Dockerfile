# this is expected to be ran from the project root
# not rest_api

FROM python:3.11.5
EXPOSE 8001

COPY ./rest_api /rest_api
COPY ./data /data
WORKDIR /rest_api

RUN pip install --upgrade --no-cache-dir pip
RUN pip install .

CMD ["fastapi", "run", "biome_rest/main.py", "--host", "0.0.0.0", "--port", "8001"]
