import os
import pathlib

from dynaconf import Dynaconf, Validator

current_directory = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))

SETTINGS = Dynaconf(
    root_path=current_directory,
    envvar_prefix="APP_CONFIG",
    settings_files=[
        "settings.toml",
        ".secrets.toml",
    ],
    environments=True,
    load_dotenv=True,
    env_switcher="ENV_FOR_APP",
    validators=[
        # Database Section
        Validator("DATABASE", "LOG_DIR", must_exist=True),
        Validator(
            "DATABASE.HOST",
            "DATABASE.PASSWORD",
            "DATABASE.USERNAME",
            "DATABASE.NAME",
            "DATABASE.PORT",
            must_exist=True,
        ),
        Validator("DATABASE.PORT", cast=int),
        Validator("DATABASE.PASSWORD", cast=str),
        # Ensure java_bin is returned as a Path instance
        Validator("LOG_DIR", must_exist=True, cast=pathlib.Path),
    ],
)


# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
