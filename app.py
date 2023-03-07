import os
from application.app_factory import create_app
from application.config_stages import stage_list
from application.config_load import application_config
from dotenv import load_dotenv

# Create app from environment variable setting. How do we best do this?

app = create_app(application_config)


def main(app):
    app.run()


if __name__ == "__main__":
    main(app)
