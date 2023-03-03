import os
from application.app_factory import create_app
from application.config import stage_list
from dotenv import load_dotenv

# Create app from environment variable setting. How do we best do this?

load_dotenv()

stage_name = os.environ.get("STAGE")

application_config = stage_list[stage_name]()
app = create_app(application_config)


def main(app):
    app.run()


if __name__ == "__main__":
    main(app)
