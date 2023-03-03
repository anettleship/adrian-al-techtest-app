from flask import Blueprint, current_app 
from . templates_init import jinja_env


t2lifestylechecker = Blueprint("t2lifesteylchecker", __name__)


@t2lifestylechecker.route("/")
def index():
    template = jinja_env.get_template("base.html")
    return template.render(title="NHS")


@t2lifestylechecker.route("/js")
def static_js():
    return current_app.send_static_file("datepicker.js")