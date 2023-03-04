import requests
import os
from dotenv import load_dotenv
from enum import Enum
from . localisation.external_api_return_states_text import return_state_localisations


class ExternalValidationHandler():
    def __init__(self, user_data):

        load_dotenv()
        self.subscription_key_name = os.environ.get("SUBSCRIPTION_KEY_NAME")
        self.subscription_key = os.environ.get("SUBSCRIPTION_KEY")
        self.api_url = os.environ.get("EXTERNAL_API_URL")

        self.return_states = Enum(
            "return_states", [
                "not_found",
                "details_not_matched",
                "not_over_sixteen",
                "found"
            ]
        )

    def call_validation_api(self, nhsnumber: str) -> requests.Response:
        data = {
            self.subscription_key_name: self.subscription_key
        }

        return requests.post(self.api_url + nhsnumber, data=data)

    def process_response(self, response: requests.Response) -> Enum:

        if response.status_code != 200:
            return self.return_states['not_found']

        # check if user_data matches data in response
        if not self.user_data_matches(response):
            return self.return_states['details_not_matched']

        # check if user date of birth is not over sixteen
        if not self.user_over_sixteen(response):
            return self.return_states['not_over_sixteen']

        return self.return_states['found']


    def user_data_matches(self, response: requests.Response) -> bool:

        result = True 

        return result

    def user_over_sixteen(self, response: requests.Response) -> bool:

        result = True

        return result
 