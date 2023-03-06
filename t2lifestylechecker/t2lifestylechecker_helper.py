
from . valid_results import external_api_valid_results
from . localisation.external_api_return_messages_text import externalvalidationhandler_message_localisations 

def get_localised_message(result_object, language):

    return externalvalidationhandler_message_localisations[language][result_object.name]