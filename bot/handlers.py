import logging

import asyncpg
from pyrogram import filters

from db import connect_to_db
from . import app
from .funnel import Funnel
from .user import User

logger = logging.getLogger('bot_logger')


@app.on_message(filters.private)
async def start(_, message):
    if message.from_user.is_self:
        return
    message_id = message.id
    user_id = message.from_user.id
    username = message.from_user.username
    conn_db = await connect_to_db()
    async with conn_db.transaction():
        try:
            user = User(user_id, username)
            if not await user.get_user(conn_db):
                logger.info(
                    f'Added new user {username}')
                await user.save_user(message_id, conn_db)

                user_db = await user.get_user(conn_db)
                funnel = Funnel(user_db.get('id'))
                await funnel.init_funnels(conn_db)
        except asyncpg.exceptions.UniqueViolationError as e:
            logger.error(e)
    await conn_db.close()
