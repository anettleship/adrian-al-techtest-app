import json
from enum import Enum


questionnaire_validity_states = Enum(
    'questionnaire_validity', [
        'not_checked',
        'not_valid',
        'valid'
    ]
)


class QuestionnaireHandler():

    def __init__(self):
        self.question_data = None
        self.questionnaire_validity = questionnaire_validity_states['not_checked']

    def load_question_data(self, question_data_path):
        with open(question_data_path, 'r') as f:
            self.question_data = json.load(f)

    def validate_question_data(self):

        self.questionnaire_validity = questionnaire_validity_states['valid']
