import json
from enum import Enum


questionnaire_validity_states = Enum(
    'questionnaire_validity', [
        'not_checked',
        'not_valid',
        'valid'
    ]
)

questionnaire_validity_messages = Enum(
    'questionnaire_validity_message', [
        'file not found at supplied path',
        'json could not be parsed',
        'all answers must have list of points equal to age range maximums plus one',
    ]
)


class QuestionnaireHandler():

    def __init__(self):
        self.question_data = None
        self.questionnaire_validity = questionnaire_validity_states['not_checked']
        self.validity_message = str() 

    def load_question_data(self, question_data_path: str):

        try:
            with open(question_data_path, 'r') as f:
                self.question_data = json.load(f)
        except FileNotFoundError:
            self.questionnaire_validity = questionnaire_validity_states['not_valid']
            self.validity_message = questionnaire_validity_messages['file not found at supplied path']
            return
        except json.decoder.JSONDecodeError:
            self.questionnaire_validity = questionnaire_validity_states['not_valid']
            self.validity_message = questionnaire_validity_messages['json could not be parsed']
            return


    def validate_question_data(self):

        valid_so_far = True

        if self.question_data == None:
            valid_so_far = False

        if not self.check_answer_points_for_all_age_ranges():
            valid_so_far = False

        if valid_so_far:
            self.questionnaire_validity = questionnaire_validity_states['valid']


    def check_answer_points_for_all_age_ranges(self):

        age_range_count = len(self.question_data['age_range_maximums'])
        points_count_per_answer = age_range_count + 1

        for question in self.question_data['questions']:
            for points_list in question['answers'].values():
                if len(points_list) != points_count_per_answer:
                    self.questionnaire_validity = questionnaire_validity_states['not_valid']
                    self.validity_message = questionnaire_validity_messages['all answers must have list of points equal to age range maximums plus one']
                    return False

        return True
