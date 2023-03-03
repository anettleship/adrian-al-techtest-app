from flask import Blueprint, current_app, send_from_directory 
from . templates_init import jinja_env

application_name = "t2lifestylechecker"

t2lifestylechecker = Blueprint(application_name, __name__)


@t2lifestylechecker.route("/")
def index():
    template = jinja_env.get_template("base.html")
    return template.render(title="NHS")


@t2lifestylechecker.route("/js/<path:filename>")
def static_js(filename):
    return send_from_directory(f'../{application_name}/static/js', filename)
