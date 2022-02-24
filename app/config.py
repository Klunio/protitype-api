# -*- coding: utf-8 -*-
# Create Time: 02/23 2022
# Author: Yunquan (Clooney) Gu

from pydantic import BaseSettings, Field


class Setting(BaseSettings):
    db_url: str = Field(..., env="DATABASE_URL")


settings = Setting()
