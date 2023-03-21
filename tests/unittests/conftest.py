import os

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from simple_web_api.model import ItemModel

# Database Initialization, popping means removing environment variable
os.environ["DB_USERNAME"] = "postgres"
os.environ["DB_DATABASE"] = "test_simple_web_api_db"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PASSWORD"] = "123456"
os.environ["DB_PORT"] = "5432"


def clear_test_db(_db_session: Session):
    try:
        _db_session.query(ItemModel).delete()
        _db_session.commit()
    except SQLAlchemyError:
        _db_session.rollback()


@pytest.fixture(scope="package")
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
