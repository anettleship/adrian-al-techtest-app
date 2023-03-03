from flask import Blueprint, current_app, render_template
from . template_setup import jinja_env


t2lifestylechecker = Blueprint("t2lifesteylchecker", __name__)

@t2lifestylechecker.route("/")
def index():

    template = jinja_env.get_template("base.html") 
    return template.render(title="NHS")