import requests
import os
from enum import Enum
from dotenv import load_dotenv
from datetime import datetime
from .t2lifestylechecker_config import external_api_login_results


class ExternalValidationHandler():
    def __init__(self, nhsnumber: str, firstname: str, lastname: str, dateofbirth: str, today=datetime.now()):

        self.nhsnumber = nhsnumber
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.today = today
        self.user_age = None
 
        load_dotenv()

    def validate_details(self) -> Enum:

        response = self.call_validation_api()

        return self.process_response(response)

    def call_validation_api(self) -> requests.Response:
        subscription_key_name = os.environ.get("SUBSCRIPTION_KEY_NAME")
        subscription_key = os.environ.get("SUBSCRIPTION_KEY")
        api_url = os.environ.get("EXTERNAL_API_URL")

        data = {
            subscription_key_name: subscription_key
        }

        return requests.get(api_url + self.nhsnumber, headers=data)

    def process_response(self, response: requests.Response) -> Enum:

        if response.status_code != 200:
            return external_api_login_results['not_found']

        # check if user_data matches data in response
        if not self.user_data_matches(response):
            return external_api_login_results['details_not_matched']

        # check if user date of birth is not over sixteen
        form_date_format_str = os.environ.get("FORM_INPUT_DATE_FORMAT_STRING")
        self.user_age = self.get_age_today(self.dateofbirth, form_date_format_str)

        if not self.user_age >= 16:
            return external_api_login_results['not_over_sixteen']

        return external_api_login_results['found']

    def get_age_today(self, dateofbirth: str, date_format_str: str) -> int:

        born = datetime.strptime(dateofbirth, date_format_str)
        today = self.today 
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def user_data_matches(self, response: requests.Response) -> bool:

        if self.make_fullname_string() != response.json()['name'].lower():
            return False

        form_date_format_str = os.environ.get("FORM_INPUT_DATE_FORMAT_STRING")
        api_date_format_str = os.environ.get("API_DATE_FORMAT_STRING")

        form_dateofbirth_dt = datetime.strptime(self.dateofbirth, form_date_format_str)
        api_dateofbirth_dt = datetime.strptime(response.json()['born'], api_date_format_str)
        if form_dateofbirth_dt != api_dateofbirth_dt:
            return False

        return True

    def make_fullname_string(self):

        firstname = self.firstname.lower()
        lastname = self.lastname.lower()
        return f'{lastname}, {firstname}'
