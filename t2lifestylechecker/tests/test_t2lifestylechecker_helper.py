import pytest
from t2lifestylechecker.valid_results import external_api_valid_results
from t2lifestylechecker.t2lifestylechecker_helper import get_localised_message
from t2lifestylechecker.localisation.external_api_return_messages_text import externalvalidationhandler_message_localisations 

validation_messages = [
    ('not_found', 'en-gb', 'Your details could not be found'),
    ('details_not_matched', 'en-gb', 'Your details could not be found'),
    ('not_over_sixteen', 'en-gb', 'You are not eligble for this service'),
    ('found', 'en-gb', 'This message is never used')
]

@pytest.mark.parametrize('result,language,message',validation_messages)
def test_get_localised_message_should_get_localised_message_for_language_code(result,language,message):

    result_object = external_api_valid_results[result]

    assert get_localised_message(result_object, language) == message

