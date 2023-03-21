import pytest

from simple_web_api.settings import DBConfig


@pytest.mark.pre_test_fixtures
def test_settings_created():
    db_settings = DBConfig()
    assert db_settings.USERNAME == "postgres"
    assert db_settings.PASSWORD == "123456"
    assert db_settings.HOST == "localhost"
    assert db_settings.DATABASE == "test_simple_web_api_db"
    assert db_settings.PORT == 5432
