FROM debian AS deno-dl

RUN apt-get update && apt-get install -y curl unzip \
    && curl -fsSL https://deno.land/install.sh | sh

FROM python:3.12-slim

WORKDIR /app

COPY --from=deno-dl /root/.deno/bin/deno /usr/local/bin/deno

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --compile --without dev -E speed

COPY . ./

CMD ["/bin/sh", "run.sh"]