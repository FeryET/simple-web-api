import unittest.mock

import pytest

import simple_web_api.crud as crud
from simple_web_api.model import ItemModel

test_items = ItemModel(description="salam", value=12), ItemModel(
    description="test", value=100
)


@pytest.mark.order(1)
@unittest.mock.patch("simple_web_api.crud.DB_SESSION", autospec=True)
def test_commit_is_called_for_create(DB_SESSION):
    crud.create_item(ItemModel(description="test", value=0))
    DB_SESSION.commit.assert_called_once()


@pytest.mark.parametrize("item", test_items)
@pytest.mark.order(2)
def test_create_item(item: ItemModel):
    assert crud.create_item(item)
