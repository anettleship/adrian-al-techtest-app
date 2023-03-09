import pytest
from t2lifestylechecker.t2lifestylechecker_config import external_api_login_results
from t2lifestylechecker.external_validation_handler_helper import get_localised_message, obfuscate_string_base64, decode_string_base64

validation_messages = [
    ('not_found', 'en-gb', 'Your details could not be found'),
    ('details_not_matched', 'en-gb', 'Your details could not be found'),
    ('not_over_sixteen', 'en-gb', 'You are not eligble for this service'),
    ('found', 'en-gb', 'This message is never used')
]

@pytest.mark.parametrize('result,language,message',validation_messages)
def test_get_localised_message_should_get_localised_message_for_language_code(result,language,message):

    result_object = external_api_login_results[result]

    assert get_localised_message(result_object, language) == message


input_strings = [
    (str(111222333)),
    (str(444555666)),
    ("Cheese")
]


@pytest.mark.parametrize('input', input_strings)
def test_obfuscate_string_base64_and_decode_string_base64_should_encode_and_decode_a_string_to_produce_the_same_output_as_input(input):

    encoded = obfuscate_string_base64(input)
    output = decode_string_base64(encoded)

    assert output == input