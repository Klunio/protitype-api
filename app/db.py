# -*- coding: utf-8 -*-
# Create Time: 01/05 2022
# Author: Yunquan (Clooney) Gu
from typing import List

from loguru import logger
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.models.Tables import Base, ItemTable
from app.models.schema import InventoryItem


class database:
    def __init__(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///inventory.db")
        self.async_session = sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def begin(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_item(self, item: InventoryItem) -> None:
        async with self.async_session() as session:
            session.add(ItemTable(
                description=item.description,
                create_time=item.create_time
            ))
            await session.commit()
        logger.info('[Database] Inserting succeed')

    async def get_all(self) -> List[InventoryItem]:
        async with self.async_session() as session:
            result = (await session.execute(select(ItemTable))).scalars()
            return [
                InventoryItem(
                    id=i.id,
                    description=i.description,
                    create_time=i.create_time
                ).dict() for i in result.all()]

    async def delete_item(self, id) -> None:
        async with self.async_session() as session:
            await session.execute(delete(ItemTable).where(ItemTable.id == id))
            await session.commit()
            logger.info('[Database] Deleting succeed')

    async def update_item(self, id: str, Description: str) -> None:
        async with self.async_session() as session:
            await session.execute(
                update(ItemTable).
                    where(ItemTable.id == id).
                    values(description=Description)
            )
            await session.commit()
        logger.info('[Database] Updating succeed')

