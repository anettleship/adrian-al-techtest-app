from t2lifestylechecker.external_validation_handler import ExternalValidationHandler
from t2lifestylechecker.valid_results import external_api_valid_results
from t2lifestylechecker.tests.test_helpers import calculate_birth_year_from_constant_age_and_birthday
from dotenv import load_dotenv
from datetime import datetime
import requests
import pytest
import json


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_ExternalValidationHandler_call_validation_api_should_return_requests_response_object():
    nhsnumber = "111222333"
    firstname = None
    lastname = None
    dateofbirth = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response = validator.call_validation_api()
    assert type(response) == requests.Response
    assert response.status_code == 200


age_calculations = [
    ('-03-31', 61, '1961-03-31'),
    ('-07-06', 39, '1983-07-06'),
    ('-01-01', 23, '2000-01-01'),
    ('-12-31', 22, '2000-12-31'),
]

@pytest.mark.parametrize("birthday_month_day,age,expected", age_calculations)
def test_calculate_birth_year_from_constant_age_and_birthday(birthday_month_day, age, expected):

    assert calculate_birth_year_from_constant_age_and_birthday(birthday_month_day, age) == expected


known_api_transactions = [
    ('123456789', 'Kent', 'Beck', '-03-31', 61, 'not_found'),
    ('111222333', 'John', 'Doe', '-01-14', 18, 'found'),
    ('111222333', 'John', 'Doe', '-01-15', 18, 'details_not_matched'),
    ('111222333', 'John', 'Doe', '-01-08', 22, 'details_not_matched'),
    ('555666777', 'Megan', 'May', '-11-14', 14, 'not_over_sixteen'),
]


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
@pytest.mark.parametrize("nhsnumber,firstname,lastname,month_day,age,expected", known_api_transactions)
def test_ExternalValidationHandler_process_response_should_return_expected_response_for_known_test_cases(
    nhsnumber, firstname, lastname, month_day, age, expected
):
    # NB: the external api's exact  date of birth varies per query, it sometimes returns a 
    # date of birth which results in an age > 16 for Megan May.

    # The above input dates of birth should be realigned with the recorded api response
    # if api responses are ever re-recorded.

    user_dateofbirth_constant_age = calculate_birth_year_from_constant_age_and_birthday(month_day, age)

    today_object = datetime.now() 
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, user_dateofbirth_constant_age, today_object)

    response = validator.call_validation_api() 
    
    assert validator.process_response(response) == external_api_valid_results[expected]


known_api_transactions_found = [
    ('111222333', 'John', 'Doe', '-01-14', 18, 'found'),
    ('555666777', 'Megan', 'May', '-11-14', 14, 'not_over_sixteen'),
]

@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
@pytest.mark.parametrize("nhsnumber,firstname,lastname,month_day,age,expected", known_api_transactions_found)
def test_ExternalValidationHandler_process_response_should_set_age_for_user_when_details_match(
    nhsnumber, firstname, lastname, month_day, age, expected
):

    user_dateofbirth_constant_age = calculate_birth_year_from_constant_age_and_birthday(month_day, age)

    today_object = datetime.now() 
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, user_dateofbirth_constant_age, today_object)

    response = validator.call_validation_api() 
    validator.process_response(response)
    
    assert validator.user_age == age 


known_api_transactions_1 = [
    ('123456789', 'Kent', 'Beck', '1961-03-31', 'not_found'),
]

@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
@pytest.mark.parametrize("nhsnumber,firstname,lastname,dateofbirth,expected", known_api_transactions_1)
def test_ExternalValidationHandler_validate_details_executes_function_sequence_correctly(
    nhsnumber, firstname, lastname, dateofbirth, expected
):
    today_object = datetime.strptime("2021-12-31", "%Y-%m-%d")
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth, today_object)
    
    assert validator.validate_details() == external_api_valid_results[expected]


birtday_inputs = [
    ("2000-01-01", "2016-01-01", 16),
    ("2000-01-31", "2017-01-30", 16),
    ("2000-01-01", "2036-06-01", 36),
    ("1900-01-01", "1916-01-01", 16),
    ("2000-02-29", "2016-02-29", 16),
    ("2000-01-01", "2015-12-31", 15),
    ("1900-01-01", "1915-01-01", 15),
    ("2000-02-29", "2016-02-28", 15),
    ("1900-01-01", "2016-01-01", 116),
]


@pytest.mark.parametrize("dateofbirth,today,expected", birtday_inputs)
def test_ExternalValidationHandler_get_age_today_should_return_correct_age(
    dateofbirth, today, expected
):
    nhsnumber = None
    firstname = None
    lastname = None

    today_object = datetime.strptime(today, "%Y-%m-%d")
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth, today_object)

    assert validator.get_age_today(dateofbirth, "%Y-%m-%d") == expected


name_inputs = [
    ("KENT", "Beck", "beck, kent"),
    ("Kent", "Beck", "beck, kent"),
    ("Kent", "BECK", "beck, kent"),
    ("kent", "beck", "beck, kent"),
    ("kEnT", "BeCk", "beck, kent"),
]


@pytest.mark.parametrize("firstname,lastname,expected", name_inputs)
def test_ExternalValidationHandler_make_fullname_string_should_not_be_case_sensitive(
    firstname, lastname, expected
):
    nhsnumber = None
    dateofbirth = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    assert validator.make_fullname_string() == expected


known_api_transactions_matches = [
    ('111222333', 'John', 'Doe', '2005-01-14', True),
    ('111222333', 'John', 'Doe', '2001-11-04', False),
    ('555666777', 'Megan', 'May', '2008-11-14', True),
    ('555666777', 'Megan', 'May', '2008-11-15', False),
]

@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
@pytest.mark.parametrize("nhsnumber,firstname,lastname,dateofbirth,expected", known_api_transactions_matches)
def test_ExternalValidationHandler_user_data_matches_should_return_correctly_for_known_cases(
    nhsnumber, firstname, lastname, dateofbirth, expected
):
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response = validator.call_validation_api()
    
    assert validator.user_data_matches(response) == expected