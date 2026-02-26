FROM python:3.12

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg

RUN curl -fsSL https://deno.land/install.sh | sh \
    && mv /root/.deno/bin/deno /usr/local/bin/deno \
    && rm -rf /root/.deno

RUN pip install --no-cache-dir -U poetry

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --with dev
