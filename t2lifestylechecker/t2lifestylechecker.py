import os
from flask import (
    Blueprint,
    current_app,
    send_from_directory,
    request,
    redirect,
    url_for,
    session,
)
from flask_login import login_required, login_user, logout_user
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from application.auth import User
from .t2lifestylechecker_config import external_api_login_results
from .external_validation_handler import ExternalValidationHandler
from .external_validation_handler_helper import (
    get_localised_message,
    obfuscate_string_base64,
)
from .questionnaire_handler import QuestionnaireHandler

application_name = "t2lifestylechecker"

t2lifestylechecker = Blueprint(application_name, __name__)

jinja_env = Environment(
    loader=PackageLoader("t2lifestylechecker"), autoescape=select_autoescape()
)


@t2lifestylechecker.route("/")
def index():
    template = jinja_env.get_template("login.html")
    form_title = os.environ.get("LOGIN_FORM_TITLE")
    validate_url = url_for(f"{application_name}.validate")
    return template.render(title=form_title, form_action_url=validate_url)


@t2lifestylechecker.route("/login")
def login():
    return redirect("/")


@t2lifestylechecker.route("/js/<path:filename>")
def static_js(filename):
    return send_from_directory(f"../{application_name}/static/js", filename)


@t2lifestylechecker.route("/validate_login", methods=["POST"])
def validate():
    nhs_number = request.form["nhs_number"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    date_of_birth = request.form["date_of_birth"]

    with current_app.app_context():
        validator = ExternalValidationHandler(
            nhs_number, first_name, last_name, date_of_birth
        )

    result = validator.validate_details()

    if not result == external_api_login_results["found"]:
        language = os.environ.get("LANGUAGE")

        questionnaire_title = os.environ.get("LOGIN_FORM_TITLE")
        template = jinja_env.get_template("message.html")
        return template.render(
            title=questionnaire_title,
            message=get_localised_message(result, language)
        )

    obfuscate_nhs_number = obfuscate_string_base64(nhs_number)
    user = User(obfuscate_nhs_number)
    session["user_age"] = validator.user_age
    login_user(user)
    return redirect("questionnaire")


@t2lifestylechecker.route("/questionnaire")
@login_required
def questionnaire():
    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler = QuestionnaireHandler(question_data_path)

    template = jinja_env.get_template("questionnaire.html")
    questionnaire_title = os.environ.get("QUESTION_FORM_TITLE")
    form_action = url_for(f"{application_name}.calculate")
    return template.render(
        title=questionnaire_title,
        form_action_url=form_action,
        questionnaire=questionnaire_handler.question_data,
    )


@t2lifestylechecker.route("/calculate_score", methods=["POST"])
@login_required
def calculate():
    age = session["user_age"]
    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler = QuestionnaireHandler(question_data_path)
    answers = list()

    for index, question in enumerate(request.form):
        if index >= len(questionnaire_handler.question_data["questions"]):
            break
        answer = request.form[question]
        answers.append(answer)

    final_message = questionnaire_handler.caluculate_message(age, answers)

    logout_user()

    questionnaire_title = os.environ.get("QUESTION_FORM_TITLE")
    template = jinja_env.get_template("message.html")
    return template.render(
        title=questionnaire_title,
        message=final_message
    )
