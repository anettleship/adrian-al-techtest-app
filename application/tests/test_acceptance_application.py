import os
from application.app_factory import create_app
import application.config as config
from dotenv import load_dotenv 
from application.config_stages import stage_list


def test_app_should_return_http_success_from_default_route():
    app = create_app(config.Testing())

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200


def test_app_should_be_able_to_load_a_valid_stage_environment_variable_from_dotenv_file():

    load_dotenv()

    stage = os.environ.get("STAGE")
    assert stage_list[stage] in stage_list.values()
