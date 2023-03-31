import unittest.mock

import pytest
from sqlalchemy.orm import Session

import simple_web_api.crud as crud
from simple_web_api.model import ItemModel

test_create_items = ItemModel(description="salam", value=12), ItemModel(
    description="test", value=100
)

test_read_items = [
    item.copy(update=dict(id=idx))
    for idx, item in enumerate(test_create_items, start=1)
]


@pytest.mark.order(1)
def test_commit_is_called_for_create():
    db_session = unittest.mock.MagicMock()
    crud.create_item(ItemModel(description="test", value=0), db_session=db_session)
    db_session.commit.assert_called_once()


@pytest.mark.parametrize("item", test_create_items)
@pytest.mark.order(2)
def test_create_item(item: ItemModel, db_session: Session):
    assert crud.create_item(item, db_session=db_session)


@pytest.mark.parametrize("item", test_read_items)
@pytest.mark.order(3)
def test_select_item_by_id(item: ItemModel, db_session: Session):
    read_item = crud.select_item_by_id(item.id, db_session=db_session)
    assert read_item is not None
    assert read_item.id == item.id


@pytest.mark.parametrize("item", test_read_items)
@pytest.mark.order(3)
def test_read_item(item: ItemModel, db_session: Session):
    assert crud.read_item(item.id, db_session=db_session).dict() == item.dict()
