import sys
import os
from flask import Blueprint, current_app, send_from_directory, request, redirect, url_for
from flask_login import login_required, login_user, current_user
from application.config_load import application_config, questionnaire_data
from . t2lifestylechecker_config import jinja_env, questionniare_handler, T2User
from . external_validation_handler import ExternalValidationHandler
from . valid_results import external_api_valid_results
from . localisation.external_api_return_messages_text import externalvalidationhandler_message_localisations
from . t2lifestylechecker_helper import get_localised_message



application_name = "t2lifestylechecker"

t2lifestylechecker = Blueprint(application_name, __name__)



@t2lifestylechecker.route("/")
def index():
    template = jinja_env.get_template("login.html")
    form_title = application_config.login_form_title
    validate_url = url_for(f'{application_name}.validate')
    return template.render(title=form_title, form_action_url=validate_url)


@t2lifestylechecker.route("/js/<path:filename>")
def static_js(filename):
    return send_from_directory(f'../{application_name}/static/js', filename)


@t2lifestylechecker.route("/validate_login", methods=["POST"])
def validate():
    
    nhsnumber = request.form["nhsnumber"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    dateofbirth = request.form["dateofbirth"]

    with current_app.app_context():
        validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    result = validator.validate_details()

    if not result == external_api_valid_results['found']:

        language = os.environ.get('LANGUAGE')
        return get_localised_message(result, language)

    user = T2User(nhsnumber)
    login_user(user)
    return redirect('questionnaire')


@t2lifestylechecker.route("/questionnaire")
@login_required
def questionnaire():

    template = jinja_env.get_template("questionnaire.html")
    questionnaire_title = application_config.question_form_title
    return template.render(title=questionnaire_title, questionnaire=questionnaire_data)