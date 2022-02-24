FROM python:3.9-slim-buster

WORKDIR /app/jukebot

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev -E speed

COPY . ./

CMD ["poetry", "run", "task", "start"]
