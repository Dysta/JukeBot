# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/
COPY --from=denoland/deno:bin-2.9.4 /deno /usr/local/bin/deno

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install --no-install-recommends -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --extra speed --no-install-project

COPY . ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --extra speed

CMD ["uv", "run", "--no-sync", "python", "-m", "jukebot"]
