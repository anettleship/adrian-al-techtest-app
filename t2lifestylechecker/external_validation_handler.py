import requests
import os
from dotenv import load_dotenv
from enum import Enum
from . localisation.external_api_return_states_text import return_state_localisations
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExternalValidationHandler():
    def __init__(self, nhsnumber: str, firstname: str, lastname: str, dateofbirth: str, today=datetime.now()):

        self.nhsnumber = nhsnumber
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.today = today
 
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

    def validate_details(self) -> Enum:

        response = self.call_validation_api()

        return self.process_response(response)



    def call_validation_api(self) -> requests.Response:
        data = {
            self.subscription_key_name: self.subscription_key
        }

        return requests.get(self.api_url + self.nhsnumber, headers=data)

    def process_response(self, response: requests.Response) -> Enum:

        if response.status_code != 200:
            return self.return_states['not_found']

        # check if user_data matches data in response
        if not self.user_data_matches(response):
            return self.return_states['details_not_matched']

        # check if user date of birth is not over sixteen
        if not self.get_age_today(self.dateofbirth) >= 16:
            return self.return_states['not_over_sixteen']

        return self.return_states['found']

    def get_age_today(self, dateofbirth) -> int:

        born = datetime.strptime(dateofbirth, "%d-%m-%Y")
        today = self.today 
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def user_data_matches(self, response: requests.Response) -> bool:

        if self.make_fullname_string() != response.json()['name'].lower():
            return False

        input_age = self.get_age_today(self.dateofbirth)
        age_from_api_response = self.get_age_today(response.json()['born'])

        if input_age != age_from_api_response:
            return False

        return True

    def make_fullname_string(self):

        firstname = self.firstname.lower()
        lastname = self.lastname.lower()
        return f'{lastname}, {firstname}'
