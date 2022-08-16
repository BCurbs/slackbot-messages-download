import asyncio
import os
import sys

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from slack_bolt.app.async_app import AsyncApp
from loguru import logger
from config import Config
from database import db
from slackbot.archive import archive_app

config = Config()
logger.remove()
logger.add(
    sys.stdout,
    format=
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
    "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=config.log_level,
    colorize=True,
    enqueue=True,
)


async def main():
    await db.init()
    app = AsyncApp(token=config.slack_app_token)
    archive_app.register_to(app)
    logger.debug("Sub-apps registered")
    await AsyncSocketModeHandler(app, config.slack_app_token).start_async()


if __name__ == "__main__":
    asyncio.run(main())
