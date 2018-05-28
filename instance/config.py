# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os
from app.libs.jsonEncoder import DateTimeEncoder
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(object):
    TESTING = os.environ.get("TESTING", False)

    RESTFUL_JSON = {'cls': DateTimeEncoder}
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", 'amqp://localhost')
    CELERY_DEFAULT_QUEUE = 'scheduler'
    CELERY_TIMEZONE = 'UTC'

    MAESTRO_MONGO_COLLECTION = os.environ.get("MAESTRO_MONGO_COLLECTION", "schedulers_control")

    MAESTRO_MONGO_DATABASE = os.environ.get("MAESTRO_MONGO_DATABASE", 'maestro-scheduler')
    MAESTRO_MONGO_URI = "mongodb://" + os.environ.get("MAESTRO_MONGO_URI", "localhost")
    MAESTRO_LOOP_TIME = int(os.environ.get("MAESTRO_LOOP_TIME", 10))


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
