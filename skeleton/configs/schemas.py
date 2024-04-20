from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConfigBase(BaseModel):
    name: str
    value: str
    ts: datetime


class ConfigAdd(ConfigBase):
    pass


class ConfigUpdate(ConfigBase):
    pass


class Config(ConfigBase):
    id: int
