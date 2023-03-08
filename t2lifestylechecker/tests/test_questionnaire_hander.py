import pytest
import os
import json
from dotenv import load_dotenv
from t2lifestylechecker.questionnaire_handler import QuestionnaireHandler, questionnaire_validity_states

def test_QuestionnaireHandler_load_question_data_should_load_three_questions_from_default_question_data_file():

    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)

    assert len(questionnaire_handler.question_data['questions']) == 3

def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_not_checked_with_not_data_loaded():

    questionnaire_handler = QuestionnaireHandler()

    questionnaire_handler.validate_question_data()

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['not_checked']


def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_valid_for_valid_question_data():

    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    questionnaire_handler.validate_question_data()

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['valid']
