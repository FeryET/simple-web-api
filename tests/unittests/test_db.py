import pytest
from sqlalchemy.orm import Session

from simple_web_api.db import DB_ENGINE
from simple_web_api.model import ItemModel


def test_db_connect(db_session: Session):
    assert db_session is not None
    assert db_session.bind == DB_ENGINE
