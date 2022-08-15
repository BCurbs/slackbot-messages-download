from typing import List

from loguru import logger
from slack_sdk.web.async_client import AsyncWebClient

from config import Config
from database import db
from slackbot.message import Message
from slackbot.subapp import SubApp

archive_app = SubApp()
config = Config()
client = AsyncWebClient(token=config.slack_bot_token)


async def fetch_all_messages(channel: str, run_limit: int = -1):
    messages: List[Message] = []
    result = await client.conversations_history(channel=channel, limit=200)
    messages.extend([Message(body) for body in result['messages']])
    i = 0
    while 'next_cursor' in result:
        if i == run_limit:
            return messages
        cursor = result['next_cursor']
        result = await client.conversations_history(channel=channel, limit=200, cursor=cursor)
        messages.extend([Message(body) for body in result['messages']])
        i += 1

    return messages


@archive_app.command('/archivechannel')
async def archive_all(ack, body):
    await ack()
    channel_id = body['channel_id']
    logger.info(f"Starting to download messages from {channel_id}")
    await client.chat_postMessage(channel=channel_id, text=f"Starting download of messages from <#{channel_id}|>.")
    logger.trace(body)
    messages: List[Message] = await fetch_all_messages(channel_id)
    await client.chat_postMessage(channel=channel_id,
                                  text=f"{len(messages)} messages downloaded, adding to database. ")
    logger.debug('Messages downloaded, adding to database. ')
    await db.database_dump_messages(messages)
    await client.chat_postMessage(channel=channel_id, text="Messages added to database. ")


@archive_app.command('/ping')
async def ping(ack, body):
    await ack()
    channel_id = body['channel_id']
    await client.chat_postMessage(channel=channel_id, text="Pong!")
    logger.success("Ping command replied to. ")