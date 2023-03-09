import os
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from . questionnaire_handler import QuestionnaireHandler

jinja_env = Environment(
    loader=PackageLoader("t2lifestylechecker"), autoescape=select_autoescape()
)

load_dotenv()
question_data_path = os.environ.get("QUESTION_DATA_PATH")
questionnaire_handler = QuestionnaireHandler(question_data_path)
