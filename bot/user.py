from datetime import datetime

import db


class User(object):
    def __init__(self, tg_id, username=None):
        self.tg_id = tg_id
        self.username = username

    @db.using_db
    async def save_user(self, last_message_id, conn):
        await conn.execute(
            'INSERT INTO "user" (user_id, username, last_message_id) VALUES ($1, $2, $3)',
            self.tg_id, self.username, last_message_id)

    @db.using_db
    async def get_user(self, conn):
        return await conn.fetchrow('SELECT * FROM "user" WHERE user_id = $1',
                                   self.tg_id)

    @db.using_db
    async def cancel_user(self, conn):
        await conn.execute(
            'UPDATE "user" SET status = 3, status_updated_at = $2 '
            'WHERE user_id = $1',
            self.tg_id, datetime.utcnow())

    @db.using_db
    async def block_user(self, conn):
        await conn.execute(
            'UPDATE "user" SET status = 2, status_updated_at = $2 '
            'WHERE user_id = $1',
            self.tg_id, datetime.utcnow())

    @db.using_db
    async def set_last_message_id(self, new_last_message_id, conn):
        await conn.execute(
            'UPDATE "user" SET last_message_id = $1 WHERE user_id = $2',
            new_last_message_id, self.tg_id)

    @classmethod
    async def get_active_users(cls):
        conn = await db.connect_to_db()
        users_db = await conn.fetch('SELECT * FROM "user" WHERE status = 1')
        await conn.close()
        for user in users_db:
            user_instance = cls(user.get('user_id'), user.get('username'))
            yield user_instance
        return

    def __str__(self):
        return f'<User: id={self.tg_id} username={self.username}>'
