"""Data models module."""

from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    """Base Sql Model class."""


class ItemModel(BaseModel):
    """Python Item Model."""

    id: Optional[int]
    description: str
    value: int

    class Config:
        """Pydantic config class for the model."""

        orm_mode = True


class ItemInDB(Base):
    """SQL Item Table/Model."""

    __tablename__ = "item_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(sa.String(200))
    value: Mapped[int]

    def update(self, item: ItemModel) -> None:
        """Update a given sql item given its corresponding python item.

        Args:
            item (ItemModel): Input ttem.
        """
        self.description = item.description
        self.value = item.value
