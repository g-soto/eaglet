import asyncio

from sqlalchemy import MetaData, Table, Column, Integer, insert, exc, select
from sqlalchemy.ext.asyncio import create_async_engine


class SQL:
    def __init__(self):
        self.async_engine = create_async_engine("sqlite+aiosqlite:///data.sqlite3", future=True, echo=True)
        self.metadata = MetaData()
        self.registered_players = Table("RegisteredPlayers", self.metadata, Column("tg_id", Integer, primary_key=True))

    async def connect(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def exists_new_players(self, tg_ids):
        async with self.async_engine.begin() as conn:
            return any(await asyncio.gather(*(self.is_new_player(conn, tg_id) for tg_id in tg_ids)))

    async def is_new_player(self, conn, tg_id):
        try:
            _ = await conn.execute(insert(self.registered_players).values(tg_id=tg_id))
            return True
        except exc.IntegrityError:
            return False
