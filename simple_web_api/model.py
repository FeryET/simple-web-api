from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    pass


class ItemModel(BaseModel):
    id: Optional[int]
    description: str
    value: int

    class Config:
        orm_mode = True


class ItemInDB(Base):
    __tablename__ = "item_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(sa.String(200))
    value: Mapped[int]

    def update(self, item: ItemModel) -> None:
        self.description = item.description
        self.value = item.value
