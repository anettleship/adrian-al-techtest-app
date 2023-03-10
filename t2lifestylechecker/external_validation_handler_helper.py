import base64

externalvalidationhandler_message_localisations = {
    "en-gb": {
        "not_found": "Your details could not be found",
        "details_not_matched": "Your details could not be found",
        "not_over_sixteen": "You are not eligible for this service",
        "found": "This message is never used",
    }
}


def get_localised_message(result_object, language):
    return externalvalidationhandler_message_localisations[language][result_object.name]


def obfuscate_string_base64(input):
    message_bytes = input.encode("ascii")
    encoded = base64.b64encode(message_bytes)

    return encoded.decode("ascii")


def decode_string_base64(encoded_input):
    base64_bytes = encoded_input.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode("ascii")
