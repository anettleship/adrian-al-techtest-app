from flask import Blueprint, current_app
import os


t2lifestylechecker = Blueprint("t2lifesteylchecker", __name__)


@t2lifestylechecker.route("/")
def index():

    secret_key = current_app.secret_key

    if secret_key != None:
        if len(secret_key) > -1:
            return "Application passed basic healthcheck"

    raise EnvironmentError("Valid Secret Key not set!")