import requests
import os
from enum import Enum
from dotenv import load_dotenv
from datetime import datetime
from .t2lifestylechecker_config import external_api_login_results


class ExternalValidationHandler:
    def __init__(
        self,
        nhs_number: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        today=datetime.now(),
    ):
        self.nhs_number = nhs_number
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
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

        data = {subscription_key_name: subscription_key}

        return requests.get(api_url + self.nhs_number, headers=data)

    def process_response(self, response: requests.Response) -> Enum:
        if response.status_code != 200:
            return external_api_login_results["not_found"]

        if not self.user_data_matches(response):
            return external_api_login_results["details_not_matched"]

        form_date_format_str = os.environ.get("FORM_INPUT_DATE_FORMAT_STRING")
        self.user_age = self.get_age_today(self.date_of_birth, form_date_format_str)

        if not self.user_age >= 16:
            return external_api_login_results["not_over_sixteen"]

        return external_api_login_results["found"]

    def get_age_today(self, date_of_birth: str, date_format_str: str) -> int:
        born = datetime.strptime(date_of_birth, date_format_str)
        today = self.today

        age_at_end_of_year = today.year - born.year
        if (today.month, today.day) < (born.month, born.day):
            age_at_end_of_year -= 1

        return age_at_end_of_year

    def user_data_matches(self, response: requests.Response) -> bool:
        if self.make_fullname_string() != response.json()["name"].lower():
            return False

        form_date_format_str = os.environ.get("FORM_INPUT_DATE_FORMAT_STRING")
        api_date_format_str = os.environ.get("API_DATE_FORMAT_STRING")

        form_date_of_birth_dt = datetime.strptime(self.date_of_birth, form_date_format_str)
        api_date_of_birth_dt = datetime.strptime(
            response.json()["born"], api_date_format_str
        )
        if form_date_of_birth_dt != api_date_of_birth_dt:
            return False

        return True

    def make_fullname_string(self):
        first_name = self.first_name.lower()
        last_name = self.last_name.lower()
        return f"{last_name}, {first_name}"
