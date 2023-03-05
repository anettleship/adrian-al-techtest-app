from t2lifestylechecker.external_validation_handler import ExternalValidationHandler
from dotenv import load_dotenv
from datetime import datetime
import requests
import pytest
import json


# TODO Use some sort of mocking for the api call? Or make a single request, then save and modify the response, then document that's what I did

def test_ExternalValidationHandler_call_validation_api_should_return_requests_response_object():
    nhsnumber = '111222333'
    firstname = None
    lastname = None
    dateofbirth = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response = validator.call_validation_api(user_data['nhsnumber']) 
    assert type(response) == requests.Response


def test_ExternalValidationHandler_call_validation_api_should_return_data_from_known_valid_query():
    nhsnumber = '111222333'
    firstname = None
    lastname = None
    dateofbirth = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response = validator.call_validation_api()
    assert response.status_code == 200 


status_codes = [
    (404, "not_found"),
    (500, "not_found"),
    (200, "found"),
]

@pytest.mark.parametrize("input,expected", status_codes)
def test_ExternalValidationHandler_process_response_should_return_one_of_four_values_in_enum(input, expected):

    nhsnumber = None
    dateofbirth = '31-03-1961'
    firstname = 'Kent' 
    lastname = 'Beck' 

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)

    response_user_data = {
        "name": "BECK, Kent",
        "born": "31-03-1961"
        }

    response = requests.Response()

    response.status_code = input

    # TODO This is the bug, need to work out how to fake a response for testing.

    response.json = json.dumps(response_user_data)

    assert validator.process_response(response) == validator.return_states[expected]


birtday_inputs = [
    ("01-01-2000", "01-01-2016", True),
    ("31-01-2000", "31-01-2016", True),
    ("01-01-1900", "01-01-1916", True),
    ("29-02-2000", "29-02-2016", True),
    ("01-01-2000", "31-12-2015", False),
    ("01-01-1900", "01-01-1915", False),
    ("29-02-2000", "28-02-2016", False),
    ("01-01-1900", "01-01-2016", True),
    ("01-01-1900", "01-01-1816", False),
]

@pytest.mark.parametrize("dateofbirth,sixteenth_birthday,expected", birtday_inputs)
def test_ExternalValidationHandler_user_over_sixteen_should_return_false_when_younger(dateofbirth, sixteenth_birthday, expected):

    nhsnumber = None
    firstname = None
    lastname = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)
    response = requests.Response()

    response.status_code = input

    sixteenth_birthday_object = datetime.strptime(sixteenth_birthday, "%d-%m-%Y")

    assert validator.user_over_sixteen(sixteenth_birthday_object) == expected


birtday_inputs_past = [
    ("01-01-2000", True),
    ("01-01-1900", True),
]


@pytest.mark.parametrize("dateofbirth,expected", birtday_inputs_past)
def test_ExternalValidationHandler_user_over_sixteen_should_return_true_from_today_for_dates_in_past(dateofbirth, expected):

    nhsnumber = None
    firstname = None
    lastname = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)
    response = requests.Response()

    response.status_code = input

    assert validator.user_over_sixteen() == expected


name_inputs = [
    ('KENT', 'Beck', 'beck, kent'),
    ('Kent', 'Beck', 'beck, kent'),
    ('Kent', 'BECK', 'beck, kent'),
    ('kent', 'beck', 'beck, kent'),
]


@pytest.mark.parametrize("firstname,lastname,expected", name_inputs)
def test_ExternalValidationHandler_user_over_sixteen_should_return_true_from_today_for_dates_in_past(firstname, lastname, expected):

    nhsnumber = None
    dateofbirth = None

    validator = ExternalValidationHandler(nhsnumber, firstname, lastname, dateofbirth)
    response = requests.Response()

    response.status_code = input

    assert validator.make_fullname_string() == expected



def test_ExternalValidationHandler_user_data_matches_should_be_tested():
    True == False