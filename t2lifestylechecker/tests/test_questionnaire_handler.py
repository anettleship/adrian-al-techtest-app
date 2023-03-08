import pytest
import os
import json
from dotenv import load_dotenv
from t2lifestylechecker.questionnaire_handler import QuestionnaireHandler, questionnaire_validity_states, questionnaire_validity_messages

def test_QuestionnaireHandler_should_set_questionnaire_validity_to_not_checked_before_data_loaded():

    questionnaire_handler = QuestionnaireHandler()

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['not_checked']


def test_QuestionnaireHandler_load_question_data_should_load_three_questions_from_default_question_data_file():

    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)

    assert len(questionnaire_handler.question_data['questions']) == 3


def test_QuestionnaireHandler_load_question_data_should_set_questionnaire_validity_to_not_valid_if_json_data_path_invalid():


    questionnaire_handler = QuestionnaireHandler()

    question_data_path = "invalid_question_data_path"
    questionnaire_handler.load_question_data(question_data_path)

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['not_valid']
    assert questionnaire_handler.validity_message == questionnaire_validity_messages['file not found at supplied path']


def test_QuestionnaireHandler_load_question_data_question_data_should_set_questionnaire_validity_to_not_valid_if_json_data_cannot_be_parsed():


    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("TEST_INVALID_DATA")
    questionnaire_handler.load_question_data(question_data_path)

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['not_valid']
    assert questionnaire_handler.validity_message == questionnaire_validity_messages['json could not be parsed']


def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_valid_if_no_issues_found():

    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    questionnaire_handler.validate_question_data()

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['valid']


def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_not_valid_if_points_list_for_any_answer_is_less_than_age_ranges_plus_one():


    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    removed_points_value = questionnaire_handler.question_data['questions'][0]['answers']['Yes'].pop()
    
    questionnaire_handler.validate_question_data()

    assert questionnaire_handler.questionnaire_validity ==  questionnaire_validity_states['not_valid']
    assert questionnaire_handler.validity_message == questionnaire_validity_messages['all answers must have list of points equal to age range maximums plus one']

# cannot parse json
# no min age
# min age not int
# no age range maximums set
# age range maximums not int
# any answer points length does not match age range maximums list + 1
# no questions property set
# questions length is 0
# question missing any of name, text, answers, and check if any fields length is 0


