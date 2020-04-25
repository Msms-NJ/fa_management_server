# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask
from celery import Celery

from . import commands
from .extensions import register_extensions
from .models import register_shellcontext
from .routes import register_blueprints


def create_app(config_object="fa_management_server.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""

    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)
    sqlalchemy_log = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_log.setLevel(logging.INFO)
    sqlalchemy_log.addHandler(handler)
