# -*- coding: utf-8 -*-

from flask_migrate import Migrate

migrate = Migrate()


@migrate.configure
def configure_alembic(config):
    # modify config object
    config.set_main_option(
        "file_template",
        "%%(year)d%%(month).2d%%(day).2d%%(hour).2d%%(minute).2d%%(second).2d_%%(rev)s_%%(slug)s",
    )
    return config
