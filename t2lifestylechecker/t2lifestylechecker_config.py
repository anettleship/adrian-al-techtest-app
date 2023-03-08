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

questionniare_handler = QuestionnaireHandler()
