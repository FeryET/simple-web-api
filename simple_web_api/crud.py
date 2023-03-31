"""Database CRUD actions module."""
import functools
from typing import Callable, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from typing_extensions import ParamSpec

from simple_web_api.db import DB_LOGGER
from simple_web_api.model import ItemInDB, ItemModel

P = ParamSpec("P")
T = TypeVar("T")


def select_item_by_id(item_id: int, db_session: Session) -> ItemInDB:
    """Select an item by its id.

    Args:
        item_id (int):
        db_session (Session):

    Returns:
        ItemInDB:
    """
    DB_LOGGER.debug(f"Selecting {item_id} from ItemInDB table.")
    return db_session.execute(select(ItemInDB).filter_by(id=item_id)).scalar_one()


def commit_at_the_end(func: Callable[P, T]) -> Callable[P, T]:
    """Commit db transactions at the end.

    Args:
        func (Callable[P, T]): to be wrapped function.

    Returns:
        Callable[P, T]: wrapped function.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, db_session, **kwargs: P.kwargs) -> T:
        DB_LOGGER.debug(f"Executing {func.__name__}.")
        result = func(*args, db_session, **kwargs)
        DB_LOGGER.debug(f"Finished executing {func.__name__}.")
        db_session.commit()
        DB_LOGGER.debug("Commited changes.")
        return result

    return wrapper


@commit_at_the_end
def create_item(item: ItemModel, db_session: Session) -> bool:
    """Create an item in db.

    Args:
        item (ItemModel):
        db_session (Session):

    Returns:
        bool: True if transaction is successful.
    """
    db_item = ItemInDB(**item.dict())
    db_session.add(db_item)
    return True


def update_item(updated_item_model: ItemModel, db_session: Session) -> bool:
    """Update an item in the db.

    Args:
        updated_item_model (ItemModel):
        db_session (Session):

    Raises:
        ValueError: If the item id is none.

    Returns:
        bool:
    """
    if updated_item_model.id is None:
        raise ValueError("Item's id cannot be None.")
    item_db: ItemInDB = select_item_by_id(updated_item_model.id)
    item_db.update(updated_item_model)
    return True


def read_item(item_id: int, db_session: Session) -> ItemModel:
    """Read an item from the db.

    Args:
        item_id (int):
        db_session (Session):

    Returns:
        ItemModel: The returned item.
    """
    return ItemModel.from_orm(select_item_by_id(item_id, db_session))


@commit_at_the_end
def delete_item(item_id: int, db_session: Session) -> bool:
    """Delete an item from the db.

    Args:
        item_id (int):
        db_session (Session):

    Returns:
        bool:
    """
    item_db: ItemInDB = select_item_by_id(item_id)
    db_session.delete(item_db)
    return True
