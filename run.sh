# Entrypoint script for JukeBot, it ensure that dependencies are in the latest version before starting the bot.
poetry config virtualenvs.create false && \
poetry install --no-root --no-interaction --no-ansi --compile --without dev -E speed && \
poetry run task start