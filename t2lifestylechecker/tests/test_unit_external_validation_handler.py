from t2lifestylechecker.external_validation_handler import ExternalValidationHandler
from dotenv import load_dotenv
import requests
import pytest


def test_ExternalValidationHandler_call_validation_api_should_return_requests_response_object():
    user_data = {
        'nhsnumber': '123456789',
    }

    validator = ExternalValidationHandler(user_data)

    response = validator.call_validation_api(user_data['nhsnumber']) 
    assert type(response) == requests.Response


status_codes = [
    (404, "not_found"),
    (500, "not_found"),
    (200, "found"),
]

@pytest.mark.parametrize("input,expected", status_codes)
def test_ExternalValidationHandler_process_response_should_return_one_of_four_values_in_enum(input, expected):

    user_data = {}

    validator = ExternalValidationHandler(user_data)
    response = requests.Response()

    response.status_code = input

    assert validator.process_response(response) == validator.return_states[expected]


user_data = {
    'nhsnumber': 'not used in this test',
    'first_name': 'Kent',
    'second_name': 'Beck',
    'date_of_birth': '31-03-1961'
}