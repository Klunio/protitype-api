# -*- coding: utf-8 -*-
# Create Time: 01/05 2022
# Author: Yunquan (Clooney) Gu

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Player(BaseModel):
    username: Optional[str] = ""
    player_id: Optional[str] = ""
    xp: Optional[int] = 0
    gold: Optional[int] = 0
