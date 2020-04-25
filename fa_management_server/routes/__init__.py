# -*- coding: utf-8 -*-
"""The routes module."""

from . import auth_api, errors_api, users_api, roles_api, data_dicts_api


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(errors_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(auth_api.blueprint)
    app.register_blueprint(roles_api.blueprint)
    app.register_blueprint(data_dicts_api.blueprint)

    @app.route("/public", methods=["POST"])
    def public():
        return "fdsafda"

    return None
