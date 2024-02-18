import asyncpg

from config import Config


async def connect_to_db():
    return await asyncpg.connect(dsn=Config.DATABASE_URL)


def using_db(func):
    async def wrapper(*args, **kwargs):
        arg_count = func.__code__.co_argcount
        conn = None
        if arg_count - len(args) == 1:
            conn = await connect_to_db()
            result = await func(*args, conn, **kwargs)
        else:
            result = await func(*args, **kwargs)
        if conn is not None:
            await conn.close()
        return result

    return wrapper
