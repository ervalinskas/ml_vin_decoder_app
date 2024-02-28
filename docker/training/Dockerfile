FROM python:3.12-bookworm AS compile-image

ENV POETRY_VERSION="1.8.0"
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /vin_decoder
COPY pyproject.toml poetry.toml poetry.lock ./

# README.md is a requisite for use of poetry and this way updates to it won't trigger a docker layer rebuild
RUN touch README.md
RUN poetry install --only common,training

# Reducing image size
FROM python:3.12-slim-bookworm AS runtime-image

ENV PROJECT_NAME="vin_decoder"

WORKDIR "/$PROJECT_NAME"

COPY --from=compile-image "/${PROJECT_NAME}/.venv" "/${PROJECT_NAME}/.venv"
COPY ./vin_decoder ./vin_decoder
COPY config.toml config.toml

ENV PATH="/${PROJECT_NAME}/.venv/bin:${PATH}"
ENV PYTHONPATH="/${PROJECT_NAME}:$PYTHONPATH"
ENV CONFIG_FILE_PATH="${PROJECT_NAME}/config.toml"
