import os

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from simple_web_api.model import ItemModel

os.environ["ENV_FOR_APP"] = "test"

# from simple_web_api.config import SETTINGS

# @pytest.fixture(scope="session", autouse=True)
# def set_test_settings():
#     SETTINGS.configure(FORCE_ENV_FOR_DYNACONF="test")


def clear_test_db(_db_session: Session):
    try:
        _db_session.query(ItemModel).delete()
        _db_session.commit()
    except SQLAlchemyError:
        _db_session.rollback()


@pytest.fixture(scope="package", autouse=True)
def db_session():
    from sqlalchemy.orm import scoped_session, sessionmaker

    from simple_web_api.db import DB_ENGINE, init_db

    init_db(DB_ENGINE)
    session = scoped_session(
        sessionmaker(
            bind=DB_ENGINE, autoflush=True, autocommit=False, expire_on_commit=True
        )
    )
    clear_test_db(session)
    yield session
    session.rollback()
    session.remove()
