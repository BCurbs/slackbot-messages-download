from decimal import Decimal
from typing import Dict

from loguru import logger
from slack_sdk.web.async_client import AsyncWebClient

from config import Config

config = Config()
user_names: Dict[str, str] = {}
client = AsyncWebClient(token=config.slack_bot_token)


class Message:
    def __init__(self, body, channel: str, channel_name):
        self.ts = Decimal(body['ts'])
        self.id = body['ts']
        self.type = body['type']
        self.user_id = body['user']
        self.channel_id = channel
        self.channel_name = channel_name
        self.text = replace_user_ids(body['text'])

    async def get_user_name(self):
        global user_names
        if self.user_id in user_names:
            return user_names[self.user_id]
        else:
            result = await client.users_info(
                user=self.user_id
            )
            logger.trace(result['user'])
            user_name = parse_user_name(result['user'])
            user_names[self.user_id] = user_name
            return user_name


def parse_user_name(profile) -> str:
    if 'real_name' in profile:
        return profile['real_name']
    else:
        return profile['name']


async def get_all_users():
    global user_names
    result = await client.users_list()
    for user in result['members']:
        user_names[user['id']] = parse_user_name(user)
    logger.debug(f"Got {len(user_names)} users")


def replace_user_ids(text: str) -> str:
    for user_id in user_names.keys():
        text = text.replace(user_id, user_names[user_id])
    return text
