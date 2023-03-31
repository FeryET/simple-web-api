"""Flask application module."""
from dynaconf import FlaskDynaconf
from flask import Flask

from simple_web_api.config import SETTINGS


def create_app():
    """Create the flask app."""
    app = Flask(__name__)
    app = FlaskDynaconf(app, dynaconf_instance=SETTINGS)
