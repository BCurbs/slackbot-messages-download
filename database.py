from typing import List, Tuple

from loguru import logger

from config import Config
import asyncpg

from slackbot.message import Message

config = Config()


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool = None

    async def init(self):
        logger.debug(f"Starting db init, connecting {config.db_url}")
        self.pool: asyncpg.Pool = await asyncpg.create_pool(config.db_url)
        logger.info(f"Database connected")
        async with self.pool.acquire() as conn:
            await conn.execute("""CREATE TABLE IF NOT EXISTS messages (
                    ts DOUBLE PRIMARY KEY,
                    id VARCHAR NOT NULL,
                    user VARCHAR NOT NULL,
                    text TEXT NOT NULL
                    )""")
        logger.debug("Created tables")

    async def new_message(self, message: Message):
        async with self.pool.acquire() as conn:
            await conn.execute("""
            INSERT OR IGNORE INTO messages(ts, id, user, text)
            VALUES($1, $2, $3, $4);
            """, message.ts, message.id, message.user, message.text)
        logger.success("Added message to database")

    async def database_dump_messages(self, messages: List[Message]):
        logger.info(f"Adding {len(messages)} messages to database")
        logger.trace(messages)
        messages_tuple: List[Tuple] = []
        for message in messages:
            messages_tuple.append((message.ts, message.id, message.user, message.text))
        async with self.pool.acquire() as conn:
            await conn.executemany("""
            INSERT OR IGNORE INTO messages(ts, id, user, text)
            VALUES($1, $2, $3, $4);
            """, messages_tuple)
        logger.success(f"Added {len(messages)} to database")


db: Database = Database()
