import pytest

from simple_web_api.config import SETTINGS


@pytest.mark.pre_test_fixtures
def test_setting_environment():
    assert SETTINGS.ENV_FOR_DYNACONF == "test"


@pytest.mark.pre_test_fixtures
def test_database_settings():
    assert SETTINGS.database.username == "postgres"
    assert SETTINGS.database.password == "123456"
    assert SETTINGS.database.host == "localhost"
    assert SETTINGS.database.name == "test_simple_web_api_db"
    assert SETTINGS.database.port == 5432
