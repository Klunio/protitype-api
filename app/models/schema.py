# -*- coding: utf-8 -*-
# Create Time: 01/05 2022
# Author: Yunquan (Clooney) Gu

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    id: Optional[int] = 0
    description: str
    create_time: datetime = Field(default_factory=datetime.now)
