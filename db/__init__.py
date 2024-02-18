import asyncpg

from config import Config


async def connect_to_db():
    return await asyncpg.connect(dsn=Config.DATABASE_URL)


def using_db(func):
    async def wrapper(*args, **kwargs):
        arg_count = func.__code__.co_argcount
        conn = await connect_to_db()
        if arg_count - len(args) == 1:

            result = await func(*args, conn, **kwargs)
        else:
            result = await func(*args, **kwargs)
        await conn.close()
        return result

    return wrapper
