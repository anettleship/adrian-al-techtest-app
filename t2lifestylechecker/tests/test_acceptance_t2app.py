from application.app_factory import create_app
import application.config as config


def test_t2lifestylechecker_should_return_http_success_from_default_route():
    app = create_app(config.Testing())

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200


def test_t2lifestylechecker_should_return_text_NHS_in_html_response_from_default_route():
    app = create_app(config.Testing())

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert "NHS" in response.text


def test_t2lifestylechecker_should_server_static_test_file_from_within_blueprint_static_js_folder():
    app = create_app(config.Testing())

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get("/js/testfile.js")
        assert response.status_code == 200
