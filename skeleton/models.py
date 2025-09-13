from dataclasses import dataclass
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

metadata = SQLModel.metadata


@dataclass
class Config(SQLModel, table=True):
    """Config class"""

    __table_args__ = (UniqueConstraint("name"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    value: str
