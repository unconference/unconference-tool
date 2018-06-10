# -*- coding: utf-8 -*-

import os
from flask import Flask, current_app
from flask.helpers import get_env
from werkzeug import import_string

from unconferencetool import commands
from unconferencetool.config import ProductionConfig, DevelopmentConfig

def create_app(config_object=False):
    app = Flask(__name__)

    if config_object != False:
        app.config.from_object(config_object)
    else:
        if get_env() == 'development':
            app.config.from_object(DevelopmentConfig)
        else:
            app.config.from_object(ProductionConfig)
    
    app.cli.add_command(commands.test)

    from unconferencetool.model import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    from flask_assets import Environment, Bundle
    assets = Environment()
    assets.init_app(app)
    css = Bundle("scss/style.scss", filters="libsass", output="style.css")
    js = Bundle("js/*.js", filters="jsmin", output="packed.js")
    with app.app_context():
        assets.append_path(os.path.abspath(os.path.join(current_app.config['APP_DIR'], 'assets')))
        assets.register("css", css)
        assets.register("js", js)

    def route_url(url_rule, import_name, **options):
        view = import_string(__name__ + '.views.' + import_name)
        app.add_url_rule(url_rule, import_name, view_func=view, **options)

    route_url('/', 'index.hello', methods=['GET','POST'])

    return app