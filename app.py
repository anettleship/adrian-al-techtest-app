import os
from flask_login import LoginManager, UserMixin
from application.auth import User, Auth
from application.app_factory import create_app
from application.config_stages import stage_list
from dotenv import load_dotenv

# Create app from environment variable setting. How do we best do this?

load_dotenv()

stage_name = os.environ.get("STAGE")

application_config = stage_list[stage_name]()
app = create_app(application_config)

auth = Auth()
load_user = auth.init_app(app)


def main(app):
    app.run()


if __name__ == "__main__":
    main(app)
