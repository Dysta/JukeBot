FROM python:3.10-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg

RUN pip install --no-cache-dir -U poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --with dev

COPY . ./
