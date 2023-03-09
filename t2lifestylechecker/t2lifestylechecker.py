import os
from flask import Blueprint, current_app, send_from_directory, request, redirect, url_for, session
from flask_login import login_required, login_user
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from application.config_load import application_config
from application.auth import User
from .t2lifestylechecker_config import external_api_valid_results
from .external_validation_handler import ExternalValidationHandler
from .external_validation_handler_helper import get_localised_message, obfuscate_string_base64
from . questionnaire_handler import QuestionnaireHandler

application_name = "t2lifestylechecker"

t2lifestylechecker = Blueprint(application_name, __name__)

jinja_env = Environment(
    loader=PackageLoader("t2lifestylechecker"), autoescape=select_autoescape()
)

load_dotenv()
question_data_path = os.environ.get("QUESTION_DATA_PATH")
questionnaire_handler = QuestionnaireHandler(question_data_path)


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

    obfuscate_nhsnumber = obfuscate_string_base64(nhsnumber)
    user = User(obfuscate_nhsnumber)
    session["user_age"] = validator.user_age
    login_user(user)
    return redirect('questionnaire')


@t2lifestylechecker.route("/questionnaire")
@login_required
def questionnaire():

    template = jinja_env.get_template("questionnaire.html")
    questionnaire_title = application_config.question_form_title
    form_action= url_for(f'{application_name}.calculate')
    return template.render(title=questionnaire_title, \
        form_action_url=form_action, questionnaire=questionnaire_handler.question_data)


@t2lifestylechecker.route("/calculate_score", methods=["POST"])
@login_required
def calculate():

    age = session['user_age']
    
    answers = list()

    for index, question in enumerate(request.form):
        if index >= len(questionnaire_handler.question_data['questions']):
            break
        answer = request.form[question] 
        answers.append(answer)

    return questionnaire_handler.caluculate_message(age, answers)