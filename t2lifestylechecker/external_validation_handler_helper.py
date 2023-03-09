
externalvalidationhandler_message_localisations = {
    'en-gb': {
        'not_found': 'Your details could not be found',
        'details_not_matched': 'Your details could not be found',
        'not_over_sixteen': 'You are not eligble for this service',
        'found': 'This message is never used',
    }
}


def get_localised_message(result_object, language):

    return externalvalidationhandler_message_localisations[language][result_object.name]