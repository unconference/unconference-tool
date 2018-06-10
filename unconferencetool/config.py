# -*- coding: utf-8 -*-

import os

class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG = False
    ASSETS_UPDATER = False
    SASS_STYLE = 'compressed'
    LIBSASS_STYLE = 'compressed'
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'error')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True
    ASSETS_MANIFEST = False
    ASSETS_CACHE = False
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True
    ASSETS_MANIFEST = False
    ASSETS_CACHE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False  # Allows form testing
