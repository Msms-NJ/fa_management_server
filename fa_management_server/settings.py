# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SECRET_KEY = env.str("SECRET_KEY")
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.

REDIS_URL = "redis://%(username)s:%(password)s@%(host)s:%(port)d/%(db)d" % {
    "username": env.str("REDIS_USERNAME", default=""),
    "password": env.str("REDIS_PASSWORD", default="password"),
    "host": env.str("REDIS_HOST", default="127.0.0.1"),
    "port": env.int("REDIS_PORT", default=6379),
    "db": env.int("REDIS_DB", default=0),
}

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = True
# DATABASE_QUERY_TIMEOUT = 0.001
