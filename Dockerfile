FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --compile --without dev -E speed

COPY . ./

CMD ["poetry", "run", "task", "start"]
