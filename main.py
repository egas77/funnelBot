import asyncio
import datetime
import logging

from pyrogram.errors import UserBlocked, UserDeactivated, UserDeactivatedBan, InputUserDeactivated

from bot import app
from bot.funnel import Funnel
from bot.user import User
from config import Config

logger = logging.getLogger('bot_logger')


async def main():
    logger.info('Bot started')
    async with app:
        while True:
            async for user in User.get_active_users():
                user_data = await user.get_user()
                user_id = user_data.get('user_id')
                user_pk = user_data.get('id')
                last_message_id = user_data.get('last_message_id')
                new_last_message_id = None
                funnel = Funnel(user_pk)

                try:
                    async for message in app.get_chat_history(user_id):
                        if message.from_user.is_self:
                            continue
                        if not message.text:
                            continue
                        message_text = message.text.lower()
                        if new_last_message_id is None:
                            new_last_message_id = message.id
                        if last_message_id >= message.id:
                            break
                        if 'прекрасно' in message_text or 'ожидать' in message_text:
                            logger.info(f'Manually cancel for user {user}')
                            await user.cancel_user()
                            await funnel.cancel_funnel()
                            break
                        if 'триггер1' in message_text:
                            if await funnel.get_level() == 2:
                                await funnel.trigger1()
                except (UserBlocked, UserDeactivated, UserDeactivatedBan, InputUserDeactivated):
                    logger.info(f'Block user {user}')
                    await user.block_user()
                    break
                except Exception as e:
                    logger.error(e)

                if new_last_message_id is not None:
                    await user.set_last_message_id(new_last_message_id)

                for msg in await funnel.get_funnel():
                    send_time = msg.get('send_time')
                    text = msg.get('text')
                    level = msg.get('level')
                    if send_time <= datetime.datetime.utcnow():
                        try:
                            result = await app.send_message(user_id, text)
                            print(result)
                            await funnel.cancel_level(level)
                            if level == 3:
                                await user.cancel_user()
                        except (UserBlocked, UserDeactivated, UserDeactivatedBan,
                                InputUserDeactivated):
                            logger.info(f'Block user {user}')
                            await user.block_user()
                        except Exception as e:
                            logger.error(e)
            await asyncio.sleep(Config.SLEEP_INTERVAL)


if __name__ == '__main__':
    app.run(main())
