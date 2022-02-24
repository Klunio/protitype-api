# -*- coding: utf-8 -*-
# Create Time: 02/22 2022
# Author: Yunquan (Clooney) Gu
from typing import List
from uuid import uuid4

from loguru import logger
from sqlalchemy import update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.Tables import Base, PlayerItem
from app.models.schema import Player


class database:
    def __init__(self):
        self.engine = create_async_engine(settings.db_url)
        self.async_session = sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def begin(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_new_player(self, username: str) -> Player:
        new_row = PlayerItem(
            username=username,
            player_id=str(uuid4()),
            xp=0, gold=0
        )
        async with self.async_session() as session:
            session.add(new_row)
            await session.commit()
            await session.refresh(new_row)

        new_player = Player(**new_row.__dict__)
        logger.info(f'[Database] Creating player [{new_player}] succeed')
        return new_player

    async def retrieve(self, id: str) -> Player:
        async with self.async_session() as session:
            row = (await session.execute(
                select(PlayerItem).where(PlayerItem.player_id == id)
            )).scalars().one()
            player = Player(**row.__dict__)
            logger.info(f'[Database] Retrieve player [{player}] succeed')
            return player

    async def update(self, id: str, updated_player: Player) -> bool:
        async with self.async_session() as session:
            result = await session.execute(
                update(PlayerItem).
                    where(PlayerItem.player_id == id).
                    values(**updated_player.dict())
            )
            await session.commit()
            logger.info('[Database] Updating done')
            return result.rowcount > 0

    async def topk(self, sortby: str, size: int) -> List[Player]:
        async with self.async_session() as session:
            result = (await session.execute(
                select(PlayerItem)
                    .order_by(PlayerItem.__dict__[sortby].desc())
                    .limit(size)
            )).fetchall()
            logger.info(f'[Database] Get top k by [{sortby}] with size [{size}]')
            return [Player(**i[0].__dict__) for i in result]
