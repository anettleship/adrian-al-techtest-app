import application
from application.app_factory import create_app
import application.config as config

def test_app_should_return_http_success_from_default_route():

    app = create_app(config.testing())

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200