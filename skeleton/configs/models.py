from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

SA = "sa"


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Config:
    """Config class"""

    __tablename__ = "configs"

    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(default=None, metadata={"sa": Column(String(50), unique=True)})
    value: str = field(default=None, metadata={"sa": Column(String(500))})
    ts: str = field(default=None, metadata={"sa": Column(TIMESTAMP)})
