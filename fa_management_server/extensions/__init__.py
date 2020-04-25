# -*- coding: utf-8 -*-
from .bcrypt_extension import bcrypt
from .cache_extension import cache
from .db_extension import db
from .login_manager_extension import login_manager
from .migrate_extension import migrate
from .redis_extension import redis_client
from .apscheduler_extension import scheduler
# from .celery_extension import make_celery
import atexit


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)
    # Enable the APScheduler directly
    scheduler.api_enabled=True
    scheduler.init_app(app)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

    return None
