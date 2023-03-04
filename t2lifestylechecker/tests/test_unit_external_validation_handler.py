from t2lifestylechecker.external_validation_handler import ExternalValidationHandler
from dotenv import load_dotenv
from datetime import datetime
import requests
import pytest
import json


# TODO Use some sort of mocking for the api call? Or make a single request, then save and modify the response, then document that's what I did

def test_ExternalValidationHandler_call_validation_api_should_return_requests_response_object():
    user_data = {
        'nhsnumber': '123456789',
    }

    validator = ExternalValidationHandler(user_data)

    response = validator.call_validation_api(user_data['nhsnumber']) 
    assert type(response) == requests.Response


def test_ExternalValidationHandler_call_validation_api_should_return_data_from_known_valid_query():
    user_data = {
        'nhsnumber': '111222333',
    }

    validator = ExternalValidationHandler(user_data)

    response = validator.call_validation_api(user_data['nhsnumber']) 
    assert response.status_code == 200 


status_codes = [
    (404, "not_found"),
    (500, "not_found"),
    (200, "found"),
]

@pytest.mark.parametrize("input,expected", status_codes)
def test_ExternalValidationHandler_process_response_should_return_one_of_four_values_in_enum(input, expected):

    user_data = {
        'first_name': 'Kent',
        'last_name': 'Beck',
        'date_of_birth': '31-03-1961'
    }

    response_user_data = {
        "name": "BECK, Kent",
        "born": "31-03-1961"
        }

    validator = ExternalValidationHandler(user_data)
    response = requests.Response()

    response.status_code = input
    # TODO This is the bug, need to work out how to fake a response for testing.
    response.json = json.dumps(response_user_data)

    assert validator.process_response(response) == validator.return_states[expected]


datestring_inputs = [
    ("1", "1", "1983", "01-01-1983"),
    ("01", "01", "1983", "01-01-1983"),
    ("31", "1", "2000", "31-01-2000"),
    ("23", "12", "2020", "23-12-2020"),
]

@pytest.mark.parametrize("day,month,year,expected", datestring_inputs)
def test_ExternalValidationHandler_make_date_string_should_conform_input_to_api_format(day, month, year, expected):

    user_data = {
        'day': day,
        'month': month,
        'year': year,
    }

    validator = ExternalValidationHandler(user_data)
    response = requests.Response()

    response.status_code = input

    assert validator.make_birthdate_string(user_data) == expected


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

    user_data = {}

    validator = ExternalValidationHandler(user_data)
    response = requests.Response()

    response.status_code = input

    assert validator.user_over_sixteen(dateofbirth, datetime.strptime(sixteenth_birthday, "%d-%m-%Y")) == expected


birtday_inputs_past = [
    ("01-01-2000", True),
    ("01-01-1900", True),
]


@pytest.mark.parametrize("dateofbirth,expected", birtday_inputs_past)
def test_ExternalValidationHandler_user_over_sixteen_should_return_true_from_today_for_dates_in_past(dateofbirth, expected):

    user_data = {}

    validator = ExternalValidationHandler(user_data)
    response = requests.Response()

    response.status_code = input

    assert validator.user_over_sixteen(dateofbirth) == expected


