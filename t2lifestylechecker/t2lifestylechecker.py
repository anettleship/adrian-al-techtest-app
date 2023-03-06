import sys
import os
from flask import Blueprint, current_app, send_from_directory, request
from . templates_init import jinja_env
from . external_validation_handler import ExternalValidationHandler
from . valid_results import external_api_valid_results
from . localisation.external_api_return_messages_text import externalvalidationhandler_message_localisations
from . t2lifestylechecker_helper import get_localised_message

application_name = "t2lifestylechecker"

t2lifestylechecker = Blueprint(application_name, __name__)


@t2lifestylechecker.route("/")
def index():
    template = jinja_env.get_template("base.html")
    return template.render(title="NHS")


@t2lifestylechecker.route("/js/<path:filename>")
def static_js(filename):
    return send_from_directory(f'../{application_name}/static/js', filename)


@t2lifestylechecker.route("/validate", methods=["POST"])
def validate():

    nhsnumber = request.form["nhsnumber"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    dateofbirth = request.form["dateofbirth"]

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    result = validator.validate_details()

    language = os.environ.get('LANGUAGE')
    return get_localised_message(result, language)
