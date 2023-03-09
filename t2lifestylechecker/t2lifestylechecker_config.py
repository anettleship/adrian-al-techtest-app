import os
from dotenv import load_dotenv
from enum import Enum
from application.auth import User
from jinja2 import Environment, PackageLoader, select_autoescape
from . questionnaire_handler import QuestionnaireHandler

class T2User(User):
    def __init__(self, id, age):
        super().__init__(id)
        self.id = id 
        self.age = age 


jinja_env = Environment(
    loader=PackageLoader("t2lifestylechecker"), autoescape=select_autoescape()
)


load_dotenv()
question_data_path = os.environ.get("QUESTION_DATA_PATH")
questionnaire_handler = QuestionnaireHandler(question_data_path)


class QuestionnaireResultStates(Enum):
    great_work = 0
    please_call = 1

