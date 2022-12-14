import urllib.request
import requests
from typing import List

from loguru import logger
from slack_sdk.web.async_client import AsyncWebClient

from config import Config
from database import db
from slackbot.message import Message, get_all_users
from slackbot.subapp import SubApp

archive_app = SubApp()
config = Config()
client = AsyncWebClient(token=config.slack_bot_token)


async def fetch_all_messages(channel: str, channel_name: str, run_limit: int = -1):
    await get_all_users()
    messages: List[Message] = []
    result = await client.conversations_history(channel=channel, limit=200)
    messages.extend([Message(body, channel, channel_name) for body in result['messages']])
    i = 0
    while 'next_cursor' in result:
        if i == run_limit:
            return messages
        cursor = result['next_cursor']
        result = await client.conversations_history(channel=channel, limit=200, cursor=cursor)
        messages.extend([Message(body, channel, channel_name) for body in result['messages']])
        i += 1

    return messages


@archive_app.command('/archivechannel')
async def archive_all(command):
    logger.info(f"Starting to download messages from {command.channel_id}")
    await client.chat_postMessage(channel=command.channel_id,
                                  text=f"Starting download of messages from <#{command.channel_id}|>.")
    logger.debug(f"Sent message to {command.channel_id}")
    messages: List[Message] = await fetch_all_messages(command.channel_id, command.channel_name)
    await client.chat_postMessage(channel=command.channel_id,
                                  text=f"{len(messages)} messages downloaded, adding to database. ")
    logger.debug('Messages downloaded, adding to database. ')
    await db.database_dump_messages(messages)
    await client.chat_postMessage(channel=command.channel_id, text="Messages added to database. ")


@archive_app.command('/downloadfiles')
async def save_files(command):
    results = await client.files_list()
    logger.debug("Saved initial files list. ")
    files = results['files']
    logger.debug(results['paging'])
    while results['paging']['pages'] > results['paging']['page']:
        results = await client.files_list(page=results['paging']['page'] + 1)
        files.extend(results['files'])
    await client.chat_postMessage(channel=command.channel_id, text=f"Starting download of {len(files)} files")
    for file in files:
        try:
            save_file(file['name'], file['url_private_download'])
        except:
            pass
    await client.chat_postMessage(channel=command.channel_id, text=f"Downloaded {len(files)} files")


def save_file(filename, url):
    logger.debug(url, filename)
    headers = {'Authorization': f'Bearer {config.slack_bot_token}'}
    r = requests.get(url, allow_redirects=True, headers=headers)
    with open('/tmp/slack_files/'+filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)



@archive_app.command('/ping')
async def ping(command):
    await client.chat_postMessage(channel=command.channel_id, text=f"<@{command.user_id}> | Pong!")
    logger.success("Ping command replied to. ")
