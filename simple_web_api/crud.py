"""Database CRUD actions module."""
import functools
from typing import Callable, TypeVar

from sqlalchemy import select
from typing_extensions import ParamSpec

from simple_web_api.db import DB_LOGGER, DB_SESSION
from simple_web_api.model import ItemInDB, ItemModel

P = ParamSpec("P")
T = TypeVar("T")


def select_item_by_id(item_id: int) -> ItemInDB:
    """Select an item by its id.

    Args:
        item_id (int):

    Returns:
        ItemInDB:
    """
    DB_LOGGER.debug(f"Selecting {item_id} from ItemInDB table.")
    return DB_SESSION.execute(select(ItemInDB).filter_by(id=item_id)).scalar_one()


def commit_at_the_end(func: Callable[P, T]) -> Callable[P, T]:
    """Commit db transactions at the end.

    Args:
        func (Callable[P, T]): to be wrapped function.

    Returns:
        Callable[P, T]: wrapped function.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        DB_LOGGER.debug(f"Executing {func.__name__}.")
        result = func(*args, **kwargs)
        DB_LOGGER.debug(f"Finished executing {func.__name__}.")
        DB_SESSION.commit()
        DB_LOGGER.debug("Commited changes.")
        return result

    return wrapper


@commit_at_the_end
def create_item(item: ItemModel) -> bool:
    """Create an item in db.

    Args:
        item (ItemModel):

    Returns:
        bool: True if transaction is successful.
    """
    db_item = ItemInDB(**item.dict())
    DB_SESSION.add(db_item)
    return True


def update_item(updated_item_model: ItemModel) -> bool:
    """Update an item in the db.

    Args:
        updated_item_model (ItemModel):

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


def read_item(item_id: int) -> ItemModel:
    """Read an item from the db.

    Args:
        item_id (int):

    Returns:
        ItemModel: The returned item.
    """
    return ItemModel.from_orm(select_item_by_id(item_id))


@commit_at_the_end
def delete_item(item_id: int) -> bool:
    """Delete an item from the db.

    Args:
        item_id (int):

    Returns:
        bool:
    """
    item_db: ItemInDB = select_item_by_id(item_id)
    DB_SESSION.delete(item_db)
    return True
