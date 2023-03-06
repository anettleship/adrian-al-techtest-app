from t2lifestylechecker.external_validation_handler import ExternalValidationHandler
from dotenv import load_dotenv
from datetime import datetime
import requests
import pytest
import json


@pytest.mark.vcr
def test_ExternalValidationHandler_call_validation_api_should_return_requests_response_object():
    nhsnumber = "111222333"
    firstname = None
    lastname = None
    dateofbirth = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response = validator.call_validation_api()
    assert type(response) == requests.Response
    assert response.status_code == 200


known_api_transactions = [
    ('123456789', 'Kent', 'Beck', '31-03-1961', 'not_found'),
    ('111222333', 'John', 'Doe', '08-01-2005', 'found'),
    ('111222333', 'John', 'Doe', '08-01-2001', 'details_not_matched'),
    ('555666777', 'Megan', 'May', '15-11-2006', 'not_over_sixteen'),
]

@pytest.mark.vcr
@pytest.mark.parametrize("nhsnumber,firstname,lastname,dateofbirth,expected", known_api_transactions)
def test_ExternalValidationHandler_process_response_should_match_known_cases(
    nhsnumber, firstname, lastname, dateofbirth, expected
):
    # NB: the external api's exact  date of birth varies per query, it sometimes returns a 
    # date of birth which results in an age > 16 for Megan May.

    # The above input dates of birth should be realigned with the recorded api response
    # if api responses are ever re-recorded.

    today = datetime.strptime("31-12-2021", "%d-%m-%Y")
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth, today)

    response = validator.call_validation_api() 
    
    assert validator.process_response(response) == validator.return_states[expected]

birtday_inputs = [
    ("01-01-2000", "01-01-2016", 16),
    ("31-01-2000", "30-01-2017", 16),
    ("01-01-2000", "01-06-2036", 36),
    ("01-01-1900", "01-01-1916", 16),
    ("29-02-2000", "29-02-2016", 16),
    ("01-01-2000", "31-12-2015", 15),
    ("01-01-1900", "01-01-1915", 15),
    ("29-02-2000", "28-02-2016", 15),
    ("01-01-1900", "01-01-2016", 116),
]


@pytest.mark.parametrize("dateofbirth,today,expected", birtday_inputs)
def test_ExternalValidationHandler_get_age_today_should_return_correct_age(
    dateofbirth, today, expected
):
    nhsnumber = None
    firstname = None
    lastname = None

    today_object = datetime.strptime(today, "%d-%m-%Y")
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth, today_object)

    assert validator.get_age_today(dateofbirth) == expected


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
    ('111222333', 'John', 'Doe', '04-11-2004', True),
    ('111222333', 'John', 'Doe', '04-11-2001', False),
    ('555666777', 'Megan', 'May', '15-11-2006', True),
]

@pytest.mark.vcr
@pytest.mark.parametrize("nhsnumber,firstname,lastname,dateofbirth,expected", known_api_transactions_matches)
def test_ExternalValidationHandler_user_data_matches_should_return_correctly_for_known_cases(
    nhsnumber, firstname, lastname, dateofbirth, expected
):
    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response = validator.call_validation_api()
    
    assert validator.user_data_matches(response) == expected
