import pytest
import os
import json
from dotenv import load_dotenv
from t2lifestylechecker.questionnaire_handler import (
    QuestionnaireHandler,
    questionnaire_validity_states,
    questionnaire_validity_messages,
)


def test_QuestionnaireHandler_should_set_questionnaire_validity_to_not_checked_before_data_loaded():
    questionnaire_handler = QuestionnaireHandler()

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["not_checked"]
    )


def test_QuestionnaireHandler_load_question_data_should_load_three_questions_from_default_question_data_file():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)

    assert len(questionnaire_handler.question_data["questions"]) == 3


def test_QuestionnaireHandler_load_question_data_should_set_questionnaire_validity_to_not_valid_if_json_data_path_invalid():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = "invalid_question_data_path"
    questionnaire_handler.load_question_data(question_data_path)

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["not_valid"]
    )
    assert (
        questionnaire_handler.validity_message
        == questionnaire_validity_messages["file not found at supplied path"]
    )


def test_QuestionnaireHandler_load_question_data_question_data_should_set_questionnaire_validity_to_not_valid_if_json_data_cannot_be_parsed():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("TEST_INVALID_DATA")
    questionnaire_handler.load_question_data(question_data_path)

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["not_valid"]
    )
    assert (
        questionnaire_handler.validity_message
        == questionnaire_validity_messages["json could not be parsed"]
    )


def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_not_valid_if_no_question_data_loaded():
    questionnaire_handler = QuestionnaireHandler()

    questionnaire_handler.validate_question_data()

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["not_valid"]
    )


def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_valid_if_no_issues_found():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    questionnaire_handler.validate_question_data()

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["valid"]
    )


def test_QuestionnaireHandler_validate_question_data_should_set_questionnaire_validity_to_not_valid_if_points_list_for_any_answer_is_less_than_age_ranges_plus_one():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    removed_points_value = questionnaire_handler.question_data["questions"][0][
        "answers"
    ]["Yes"].pop()

    questionnaire_handler.validate_question_data()

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["not_valid"]
    )
    assert (
        questionnaire_handler.validity_message
        == questionnaire_validity_messages[
            "all answers must have list of points equal to age range maximums plus one"
        ]
    )


def test_QuestionnaireHandler_check_answer_points_for_all_age_ranges_should_return_false_if_points_list_for_any_answer_is_less_than_age_ranges_len_plus_one():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    removed_points_value = questionnaire_handler.question_data["questions"][0]["answers"]["Yes"].pop()

    assert questionnaire_handler.check_answer_points_for_all_age_ranges() == False


def test_QuestionnaireHandler_check_answer_points_for_all_age_ranges_should_return_true_if_points_list_for_all_answers_match_age_ranges_len_plus_one():
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)

    assert questionnaire_handler.check_answer_points_for_all_age_ranges() == True


age_range_input_1 = [
    (16, [21, 40, 64], 0),
    (21, [21, 40, 64], 0),
    (22, [21, 40, 64], 1),
    (40, [21, 40, 64], 1),
    (41, [21, 40, 64], 2),
    (64, [21, 40, 64], 2),
    (1, [1, 2], 0),
    (2, [1, 2], 1),
]


@pytest.mark.parametrize("age,age_ranges,expected", age_range_input_1)
def test_QuestionnaireHandler_get_age_index_should_return_index_of_list_matching_smallest_list_item_greater_than_or_equal_to_input_age(
    age, age_ranges, expected
):
    questionnaire_handler = QuestionnaireHandler()

    assert questionnaire_handler.get_age_index(age, age_ranges) == expected


age_range_input_2 = [
    (65, [21, 40, 64], 3),
    (85, [21, 40, 64], 3),
    (3, [1, 2], 2),
]


@pytest.mark.parametrize("age,age_ranges,expected", age_range_input_2)
def test_QuestionnaireHandler_get_age_index_should_return_last_index_plus_one_of_input_list_where_input_greater_than_all_list_items(
    age, age_ranges, expected
):
    questionnaire_handler = QuestionnaireHandler()

    assert questionnaire_handler.get_age_index(age, age_ranges) == expected


known_points_for_answers = [
    (16, ["No", "No", "Yes"], 0),
    (66, ["No", "No", "Yes"], 0),
    (16, ["Yes", "No", "Yes"], 1),
    (16, ["Yes", "Yes", "Yes"], 3),
    (16, ["Yes", "Yes", "No"], 4),
    (21, ["Yes", "Yes", "No"], 4),
    (22, ["Yes", "Yes", "No"], 7),
    (40, ["Yes", "Yes", "No"], 7),
    (41, ["No", "No", "No"], 2),
    (65, ["No", "No", "No"], 1),
    (65, ["Yes", "Yes", "No"], 7),
    (85, ["No", "No", "No"], 1),
]


@pytest.mark.parametrize("age,answers,expected", known_points_for_answers)
def test_QuestionnaireHandler_calculate_points_should_return_correct_points_for_test_question_data_given_age_range_and_answers(
    age, answers, expected
):
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    questionnaire_handler.validate_question_data()

    assert questionnaire_handler.calculate_points(age, answers) == expected


def test_QuestionnaireHandler_should_load_and_validate_questionnaire_data_automatically_when_initialised_with_a_question_data_path():
    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler = QuestionnaireHandler(question_data_path)

    assert (
        questionnaire_handler.questionnaire_validity
        == questionnaire_validity_states["valid"]
    )


known_message_for_points = [
    (0, "en-gb", "great_work"),
    (3, "en-gb", "great_work"),
    (4, "en-gb", "please_call"),
    (88, "en-gb", "please_call"),
]


@pytest.mark.parametrize("points,language,expected", known_message_for_points)
def test_QuestionnaireHandler_get_message_from_points_should_return_correct_message_for_test_question_data_given_age_range_and_answers(
    points, language, expected
):
    questionnaire_handler = QuestionnaireHandler()

    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler.load_question_data(question_data_path)
    questionnaire_handler.validate_question_data()
    message = questionnaire_handler.get_message_from_points(points)

    assert (
        message == questionnaire_handler.question_data["messages"][language][expected]
    )


def test_QuestionnaireHandler_should_function_fully_when_initialised_with_a_question_data_path_and_calculate_message_is_called():
    question_data_path = os.environ.get("QUESTION_DATA_PATH")
    questionnaire_handler = QuestionnaireHandler(question_data_path)

    age = 16
    answers = ["No", "No", "Yes"]
    expected = "Thank you for answering our questions, we don't need to see you at this time. Keep up the good work!"

    message = questionnaire_handler.caluculate_message(age, answers)

    assert message == expected
