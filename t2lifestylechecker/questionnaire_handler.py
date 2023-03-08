import json

class QuestionnaireHandler():

    def __init__(self):
        self.question_data = None

    def load_question_data(self, question_data_path):
        with open(question_data_path, 'r') as f:
            self.question_data = json.load(f)


