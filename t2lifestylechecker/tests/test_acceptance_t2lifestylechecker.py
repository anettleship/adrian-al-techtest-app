import pytest
from flask import url_for
from flask_login import current_user
from application.app_factory import create_app
from application.auth import Auth
import application.config as config


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["Ocp-Apim-Subscription-Key"]}


def test_t2lifestylechecker_should_return_http_success_from_default_route():
    app = create_app(config.Testing())

    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200


def test_t2lifestylechecker_should_return_text_NHS_in_html_response_from_default_route():
    app = create_app(config.Testing())

    with app.test_client() as test_client:
        response = test_client.get("/")
        assert "NHS" in response.text


def test_t2lifestylechecker_should_server_static_test_file_from_within_blueprint_static_js_folder():
    app = create_app(config.Testing())

    with app.test_client() as test_client:
        response = test_client.get("/js/testfile.js")
        assert response.status_code == 200


@pytest.mark.vcr
def test_t2lifestylechecker_validate_route_should_return_response_to_post_data():
    app = create_app(config.Testing())

    form_data = {
        'nhsnumber': '123456789',
        'firstname': 'Kent',
        'lastname': 'Beck',
        'dateofbirth': '1961-03-31',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate", data=form_data)
        assert response.status_code == 200

@pytest.mark.vcr
def test_t2lifestylechecker_validate_route_should_return_not_found_message_for_invalid_user():
    app = create_app(config.Testing())

    form_data = {
        'nhsnumber': '123456789',
        'firstname': 'Kent',
        'lastname': 'Beck',
        'dateofbirth': '1961-03-31',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate", data=form_data)
        assert "Your details could not be found" in response.text


@pytest.mark.vcr
def test_t2lifestylechecker_validate_route_should_return_not_found_for_details_not_matched():
    app = create_app(config.Testing())

    form_data = {
        'nhsnumber': '111222333',
        'firstname': 'Kent',
        'lastname': 'Beck',
        'dateofbirth': '31-03-1961',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate", data=form_data)
        assert "Your details could not be found" in response.text


@pytest.mark.vcr
def test_t2lifestylechecker_validate_route_should_return_not_over_sixteen_for_under_sixteens():
    app = create_app(config.Testing())

    form_data = {
        'nhsnumber': '555666777',
        'firstname': 'Megan',
        'lastname': 'May',
        'dateofbirth': '2006-11-15',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate", data=form_data)
        assert "Your details could not be found" in response.text


@pytest.mark.vcr
def test_t2lifestylechecker_validate_route_should_log_user_in_when_details_match():
    app = create_app(config.Testing())

    form_data = {
        'nhsnumber': '444555666',
        'firstname': 'Charles',
        'lastname': 'Bond',
        'dateofbirth': '1953-02-28',
    }

    with app.test_client() as test_client:
        response = test_client.post("/validate", data=form_data)
        assert current_user.is_authenticated