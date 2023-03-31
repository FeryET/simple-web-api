"""Database module."""

from loguru import logger
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from simple_web_api.config import SETTINGS

logger.add(
    sink=SETTINGS.log_dir / "db.log",
    filter=lambda record: "database" in record["extra"],
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level="DEBUG",
)
DB_LOGGER = logger.bind(database=True)

DB_ENGINE = create_engine(
    url=URL.create(
        username=SETTINGS.database.username,
        password=SETTINGS.database.password,
        host=SETTINGS.database.host,
        database=SETTINGS.database.name,
        port=SETTINGS.database.port,
        drivername="postgresql+psycopg2",
    )
)

DB_SESSION = scoped_session(
    sessionmaker(bind=DB_ENGINE, autoflush=True, autocommit=False)
)


def init_db(engine: Engine):
    """Initialize database by the given engine.

    Args:
        engine (Engine): The db engine.
    """
    import simple_web_api.model  # noqa:
    from simple_web_api.model import Base

    DB_LOGGER.info("Initializing database.")
    Base.metadata.create_all(bind=engine)
    DB_LOGGER.info("SQLAlchemy tables created.")
