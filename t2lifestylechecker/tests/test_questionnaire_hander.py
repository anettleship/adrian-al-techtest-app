import pytest
import os
import json
from dotenv import load_dotenv
from t2lifestylechecker.questionnaire_handler import QuestionnaireHandler

def test_QuestionnaireHandler_load_question_data_should_load_three_questions_from_default_question_data_file():

    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")

    questionnaire_handler.load_question_data(question_data_path)

    assert len(questionnaire_handler.question_data['questions']) == 3