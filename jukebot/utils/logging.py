from __future__ import annotations

import datetime
import logging
import os

from loguru import logger

from jukebot.listeners import InterceptHandler

from .environment import Environment


def set_logging(
    jukebot_loglevel: int,
    /,
    intercept_disnake_log: bool = True,
    disnake_loglevel: int = logging.INFO,
):
    logger.info(f"Environment is set to '{os.environ['ENVIRONMENT']}'.")
    logger.info(f"Jukebot log messages with level {jukebot_loglevel}.")

    if intercept_disnake_log:
        logger.info(f"Intercepting disnake log messages with level {disnake_loglevel}.")
        logging.basicConfig(handlers=[InterceptHandler()], level=disnake_loglevel)

    if os.environ["ENVIRONMENT"] == Environment.DEVELOPMENT:
        pass
    elif os.environ["ENVIRONMENT"] == Environment.PRODUCTION:
        logger.remove()
        path: str = os.environ["LOGS_PATH"] if "LOGS_PATH" in os.environ else "./logs"
        fmt = "{time:YYYY-MM-DD at HH:mm:ss} || {level} || {name} ||  {message}"
        logger.add(
            f"{path}/log-{datetime.datetime.now():%Y-%m-%d}.log",
            level=jukebot_loglevel,
            format=fmt,
            rotation="01:00",
            retention="10 days",
            enqueue=True,
            mode="w",
            encoding="utf-8",
        )
    else:
        logger.error(f"Unknown environment {os.environ['ENVIRONMENT']}.")
        exit(1)
