# -*- coding: utf-8 -*-
"""Create an application instance."""
from fa_management_server.app import create_app
# from fa_management_server.extensions import make_celery


app = create_app()
# celery = make_celery(app)
