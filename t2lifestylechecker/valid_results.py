from enum import Enum

external_api_valid_results = Enum(
    'valid_results', [
        'not_found',
        'details_not_matched',
        'not_over_sixteen',
        'found'
    ]
)