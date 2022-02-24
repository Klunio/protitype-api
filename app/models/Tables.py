# -*- coding: utf-8 -*-
# Create Time: 02/22 2022
# Author: Yunquan (Clooney) Gu

from sqlalchemy import Column, Integer, VARCHAR

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Base.metadata.schema = 'main'


class PlayerItem(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(255))
    player_id = Column(VARCHAR(255), unique=True)
    xp = Column(Integer)
    gold = Column(Integer)
