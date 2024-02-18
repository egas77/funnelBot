from datetime import datetime, timedelta

import db
from config import Config


class Funnel(object):
    def __init__(self, user_id):
        self.user_id = user_id

    @db.using_db
    async def init_funnels(self, conn):
        now_date_time = datetime.utcnow()

        if Config.DEBUG:
            step_1_date_time = now_date_time + timedelta(minutes=1)
            step_2_date_time = step_1_date_time + timedelta(minutes=1)
            step_3_date_time = step_2_date_time + timedelta(minutes=1)
        else:
            step_1_date_time = now_date_time + timedelta(minutes=6)
            step_2_date_time = step_1_date_time + timedelta(minutes=39)
            step_3_date_time = step_2_date_time + timedelta(days=1, hours=2)

        async with conn.transaction():
            await conn.execute(
                'INSERT INTO funnel (user_id, send_time, text, status, level) '
                'VALUES ($1, $2, $3, $4, $5)',
                self.user_id, step_1_date_time, 'Текст1', 1, 1
            )
            await conn.execute(
                'INSERT INTO funnel (user_id, send_time, text, status, level) '
                'VALUES ($1, $2, $3, $4, $5)',
                self.user_id, step_2_date_time, 'Текст2', 1, 2
            )
            await conn.execute(
                'INSERT INTO funnel (user_id, send_time, text, status, level) '
                'VALUES ($1, $2, $3, $4, $5)',
                self.user_id, step_3_date_time, 'Текст3', 1, 3
            )

    @db.using_db
    async def get_funnel_full(self, conn):
        funnel = await conn.fetch('SELECT * FROM funnel WHERE user_id = $1', self.user_id)
        return funnel

    @db.using_db
    async def get_funnel(self, conn):
        funnel = await conn.fetch('SELECT * FROM funnel WHERE user_id = $1 AND status = 1',
                                  self.user_id)
        return funnel

    async def get_level(self):
        funnel = await self.get_funnel()
        active_levels = list(map(lambda f: f.get('level'), funnel))
        if active_levels:
            return min(active_levels)
        return None

    @db.using_db
    async def cancel_funnel(self, conn):
        await conn.execute(
            'UPDATE "funnel" SET status = 3, status_updated_at = $2 '
            'WHERE user_id = $1 AND status = 1',
            self.user_id, datetime.utcnow())

    @db.using_db
    async def cancel_level(self, level, conn):
        await conn.execute(
            'UPDATE "funnel" SET status = 3, status_updated_at = $3 '
            'WHERE user_id = $1 AND level = $2 AND status = 1',
            self.user_id, level, datetime.utcnow()
        )

    @db.using_db
    async def trigger1(self, conn):
        await self.cancel_level(2, conn)
        time_now = datetime.utcnow()
        if Config.DEBUG:
            new_sent_time = time_now + timedelta(seconds=5)
        else:
            new_sent_time = time_now + timedelta(days=1, hours=2)

        await conn.execute(
            'UPDATE "funnel" SET send_time = $2 '
            'WHERE status = 1 AND level = 3 AND user_id = $1',
            self.user_id, new_sent_time
        )
