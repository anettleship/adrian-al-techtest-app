import requests
import os
from dotenv import load_dotenv
from enum import Enum
from . localisation.external_api_return_states_text import return_state_localisations
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExternalValidationHandler():
    def __init__(self, user_data):

        load_dotenv()
        self.user_data = user_data
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

        return requests.get(self.api_url + nhsnumber, headers=data)

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

        firstname = self.user_data['first_name'].lower()
        lastname = self.user_data['last_name'].lower()
        fullname = f'{lastname}, {firstname}'

        if fullname != response.json()['name'].lower():
            return False

        date_of_birth = self.make_birthdate_string(self.user_data)

        if date_of_birth != response.json['born']:
            return False

        return True

    def user_over_sixteen(self, date_of_birth: datetime, today=datetime.now()) -> bool:

        date_object = datetime.strptime(date_of_birth, "%d-%m-%Y")
        date_object_plus_sixteen = date_object + relativedelta(years=16)

        if date_object_plus_sixteen > today:
            return False

        return True

    def make_birthdate_string(self, user_data: dict) -> str:

        day = f"{int(self.user_data['day']):02}"
        month = f"{int(self.user_data['month']):02}"
        year = f"{self.user_data['year']}"
        return f'{day}-{month}-{year}'
