from flask import Flask

from t2lifestylechecker.t2app import t2lifestylechecker


def create_app(config):
    """
    Application Factory function to instantiate an application from a given config class defined in config.py
    """

    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)

    return app


def register_blueprints(app):

    app.register_blueprint(t2lifestylechecker, url_prefix="/")

    return app
