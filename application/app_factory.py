import os
from flask import Flask
from application.auth import Auth
from t2lifestylechecker.t2lifestylechecker import t2lifestylechecker


def create_app(application_config):
    """
    Application Factory function to instantiate an application from a given config class defined in config.py
    """

    app = Flask(__name__)
    app.config.from_object(application_config)
    register_blueprints(app)

    auth = Auth()
    load_user = auth.init_app(app)

    return app


def register_blueprints(app):

    app.register_blueprint(t2lifestylechecker, url_prefix="/")

    return app
