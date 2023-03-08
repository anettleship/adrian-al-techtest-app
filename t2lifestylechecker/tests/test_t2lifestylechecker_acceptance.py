import pytest
from flask import current_app, session
from flask_login import current_user, login_user, LoginManager
from application.app_factory import create_app
from application.auth import Auth, User
from application.config_load import application_config, questionnaire_data
import application.config as config
from bs4 import BeautifulSoup



def test_t2lifestylechecker_index_route_should_return_sucess_with_expected_html_elements():
    app = create_app(config.Testing())

    form_title = application_config.login_form_title
    
    with app.test_client() as test_client:
        response = test_client.get("/")

    soup = BeautifulSoup(response.data, 'html.parser')
    
    assert response.status_code == 200
    assert soup.title.string == form_title 
    assert soup.find(name="input", attrs={"name": "firstname"})
    assert soup.find(name="input", attrs={"name": "lastname"})
    assert soup.find(name="input", attrs={"name": "dateofbirth"})
    assert soup.find(name="button", attrs={"name": "submit"}) 


def test_t2lifestylechecker_should_server_static_test_file_from_within_blueprint_static_js_folder():
    app = create_app(config.Testing())

    with app.test_client() as test_client:
        response = test_client.get("/js/testfile.js")
    assert response.status_code == 200


@pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"]))
def test_t2lifestylechecker_validate_route_should_return_success_from_post_request():
    app = create_app(config.Testing())

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
    app = create_app(config.Testing())

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
    app = create_app(config.Testing())

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
    app = create_app(config.Testing())

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
    app = create_app(config.Testing())

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
def test_t2lifestylechecker_validate_route_should_return_current_user_with_age_and_id():
    app = create_app(config.Testing())

    form_data = {
        'nhsnumber': '444555666',
        'firstname': 'Charles',
        'lastname': 'Bond',
        'dateofbirth': '1952-07-18',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate_login", data=form_data)
        assert current_user.age == 70
        assert current_user.id == form_data['nhsnumber']


def test_t2lifestylechecker_questionnaire_route_should_return_unauthorized_when_user_not_logged_in():
    app = create_app(config.Testing())

    question_form_title = application_config.question_form_title
    
    with app.test_client() as test_client:
        response = test_client.get("/questionnaire")

    assert response.status_code == 401 


def test_t2lifestylechecker_questionnaire_route_should_return_sucesss_for_logged_in_user():
    app = create_app(config.Testing())

    question_form_title = application_config.question_form_title
    
    with app.test_request_context("/questionnaire", method="GET"):
        with app.test_client() as test_client:
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.get("/questionnaire")
    
            assert response.status_code == 200


def test_t2lifestylechecker_questionnaire_route_should_return_all_question_and_answer_html_elements_for_logged_in_user():
    app = create_app(config.Testing())

    question_form_title = application_config.question_form_title
    
    with app.test_request_context("/validate_login", method="POST"):
        with app.test_client() as test_client:
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.get("/questionnaire")

            soup = BeautifulSoup(response.data, 'html.parser')
    
            assert soup.title.string == question_form_title 

            for question in questionnaire_data['questions']:
                assert soup.find(id=question['name'])
                for answer in question['answers']:
                    assert len(soup.find_all('input', {'type': 'radio', 'name': f"{question['name']}.{answer}"})) == 1

            assert soup.find(name="button", attrs={"name": "submit"})

def test_t2lifestylechecker_calculate_score_route_should_return_success_from_post_request_for_logged_in_user():
    app = create_app(config.Testing())

    with app.test_request_context("/validate_login", method="POST"):
        with app.test_client() as test_client:
            test_user = User('123456789')
            login_user(test_user)
            response = test_client.post("/calculate_score")

    assert response.status_code == 200


def test_t2lifestylechecker_calculate_score_route_should_return_unauthorised_when_user_not_logged_in():
    app = create_app(config.Testing())

    with app.test_client() as test_client:
        response = test_client.post("/calculate_score")

    assert response.status_code == 401 