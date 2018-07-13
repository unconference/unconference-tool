# -*- coding: utf-8 -*-
"""Test configs."""
from unconferencetool import create_app
from unconferencetool.config import DevelopmentConfig, ProductionConfig


def test_production_config():
    """Production config."""
    app = create_app(ProductionConfig)
    assert app.config['DEBUG'] is False


def test_dev_config():
    """Development config."""
    app = create_app(DevelopmentConfig)
    assert app.config['DEBUG'] is True
    assert app.config['ASSETS_CACHE'] is False
