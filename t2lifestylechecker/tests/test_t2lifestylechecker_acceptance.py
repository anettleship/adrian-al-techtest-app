import os
import pytest
from flask import url_for, session
from flask_login import current_user, login_user
from application.config import Config
from application.app_factory import create_app
from application.auth import User
from application.config_stages import Stage
from t2lifestylechecker.t2lifestylechecker import questionnaire_handler
from t2lifestylechecker.external_validation_handler_helper import obfuscate_string_base64
from bs4 import BeautifulSoup



def test_t2lifestylechecker_index_route_should_return_sucess_with_expected_html_elements():
    app = create_app(Config(Stage.testing))

    form_title =  os.environ.get("LOGIN_FORM_TITLE")

    with app.test_client() as test_client:
        response = test_client.get("/")

        soup = BeautifulSoup(response.data, 'html.parser')
        assert response.status_code == 200
        assert soup.title.string == form_title 
        assert soup.find(name="input", attrs={"name": "firstname"})
        assert soup.find(name="input", attrs={"name": "lastname"})
        assert soup.find(name="input", attrs={"name": "dateofbirth"})
        assert soup.find(name="button", attrs={"name": "submit"}) 
        assert soup.find('form', {'action': url_for('t2lifestylechecker.validate'), 'method': 'post'})


def test_t2lifestylechecker_should_server_static_test_file_from_within_blueprint_static_js_folder():
    app = create_app(Config(Stage.testing))

    with app.test_client() as test_client:
        response = test_client.get("/js/testfile.js")
    assert response.status_code == 200


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_return_success_from_post_request():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '123456789',
        'firstname': 'Kent',
        'lastname': 'Beck',
        'dateofbirth': '1961-03-31',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
    assert response.status_code == 200

@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_return_not_found_message_for_invalid_user():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '123456789',
        'firstname': 'Kent',
        'lastname': 'Beck',
        'dateofbirth': '1961-03-31',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
    assert "Your details could not be found" in response.text


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_return_not_found_for_details_not_matched():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '111222333',
        'firstname': 'Kent',
        'lastname': 'Beck',
        'dateofbirth': '31-03-1961',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
    assert "Your details could not be found" in response.text


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_return_not_over_sixteen_for_under_sixteens():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '555666777',
        'firstname': 'Megan',
        'lastname': 'May',
        'dateofbirth': '2008-11-14',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
    assert 'You are not eligble for this service' in response.text


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_log_user_in_when_details_match():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '444555666',
        'firstname': 'Charles',
        'lastname': 'Bond',
        'dateofbirth': '1952-07-18',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
        assert current_user.is_authenticated


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_set_current_user_id_with_obfuscated_nhsnumber():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '444555666',
        'firstname': 'Charles',
        'lastname': 'Bond',
        'dateofbirth': '1952-07-18',
    }

    with app.test_client() as test_client:
        test_client.post("/validate_login", data=form_data)
        assert current_user.id == obfuscate_string_base64(form_data['nhsnumber'])
    
    
@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_set_session_with_user_age():
    app = create_app(Config(Stage.testing))

    form_data = {
        'nhsnumber': '444555666',
        'firstname': 'Charles',
        'lastname': 'Bond',
        'dateofbirth': '1952-07-18',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
        assert session['user_age'] == 70
    


def test_t2lifestylechecker_questionnaire_route_should_return_unauthorized_when_user_not_logged_in():
    app = create_app(Config(Stage.testing))

    with app.test_client() as test_client:
        response = test_client.get("/questionnaire")

    assert response.status_code == 401 


def test_t2lifestylechecker_questionnaire_route_should_return_sucesss_for_logged_in_user():
    app = create_app(Config(Stage.testing))

    with app.test_request_context("/questionnaire", method="GET"):
        with app.test_client() as test_client:
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.get("/questionnaire")
    
            assert response.status_code == 200


def test_t2lifestylechecker_questionnaire_route_should_return_all_question_and_answer_html_elements_for_logged_in_user():
    app = create_app(Config(Stage.testing))

    question_form_title = os.environ.get("QUESTION_FORM_TITLE")  
    
    with app.test_request_context("/validate_login", method="POST"):
        with app.test_client() as test_client:
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.get("/questionnaire")

            soup = BeautifulSoup(response.data, 'html.parser')
    
            assert soup.title.string == question_form_title 

            for question in questionnaire_handler.question_data['questions']:
                assert soup.find(id=question['name'])
                for answer in question['answers']:
                    assert len(soup.find_all('input', {'type': 'radio', 'name': f"{question['name']}"})) == 2 

            assert soup.find(name="button", attrs={"name": "submit"})
            assert soup.find('form', {'action': url_for('t2lifestylechecker.calculate'), 'method': 'post'})

def test_t2lifestylechecker_calculate_score_route_should_return_success_from_post_request_for_logged_in_user_with_age_set_in_session():
    app = create_app(Config(Stage.testing))

    with app.test_request_context("/validate_login", method="POST"):
        with app.test_client() as test_client:
            with test_client.session_transaction() as session:
                session['user_age'] = 16
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.post("/calculate_score")

    assert response.status_code == 200


def test_t2lifestylechecker_calculate_score_route_should_return_unauthorised_when_user_not_logged_in():
    app = create_app(Config(Stage.testing))

    with app.test_client() as test_client:
        response = test_client.post("/calculate_score")

    assert response.status_code == 401 


known_questionnaire_result_for_age_and_answers = [
    (16, ["No", "No", "Yes"], 0, 'great_work'),
    (66, ["No", "No", "Yes"], 0, 'great_work'),
    (16, ["Yes", "No", "Yes"], 1, 'great_work'),
    (16, ["Yes", "Yes", "Yes"], 3, 'great_work'),
    (16, ["Yes", "Yes", "No"], 4, 'please_call'),
    (21, ["Yes", "Yes", "No"], 4, 'please_call'),
    (22, ["Yes", "Yes", "No"], 7, 'please_call'),
    (40, ["Yes", "Yes", "No"], 7, 'please_call'),
    (41, ["No", "No", "No"], 2, 'great_work'),
    (65, ["No", "No", "No"], 1, 'great_work'),
    (65, ["Yes", "Yes", "No"], 7, 'please_call'),
    (85, ["No", "No", "No"], 1, 'great_work'),
]

@pytest.mark.parametrize("age,answers,score,expected", known_questionnaire_result_for_age_and_answers)
def test_t2lifestylechecker_calculate_score_route_should_return_correct_message_for_given_test_user_ages_and_answers_with_logged_in_user_and_age_set_in_seesion(age, answers, score, expected):
    app = create_app(Config(Stage.testing))
    questionnaire_handler
    form_data = {
        'Q1': f'{answers[0]}',
        'Q2': f'{answers[1]}',
        'Q3': f'{answers[2]}',
        'Submit': '',
    }

    language = 'en-gb'

    with app.test_request_context("/validate_login", method="POST"):
        with app.test_client() as test_client:
            with test_client.session_transaction() as session:
                session['user_age'] = age
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.post("/calculate_score", data=form_data)
    
    expected_message = questionnaire_handler.question_data['messages'][language][expected]

    assert expected_message in response.text


def test_t2lifestylechecker_calculate_score_route_should_log_user_out_after_returning_message():
    app = create_app(Config(Stage.testing))
    questionnaire_handler
    form_data = {
        'Q1': 'Yes',
        'Q2': 'Yes',
        'Q3': 'Yes',
        'Submit': '',
    }

    with app.test_request_context("/validate_login", method="POST"):
        with app.test_client() as test_client:
            with test_client.session_transaction() as session:
                session['user_age'] = 70 
            test_user = User('123456789')
            login_user(test_user)
            test_client.post("/calculate_score", data=form_data)
    
            assert not current_user.is_authenticated

