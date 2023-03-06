import os
from flask_login import LoginManager, UserMixin
from application.app_factory import create_app
from application.config_stages import stage_list
from dotenv import load_dotenv

# Create app from environment variable setting. How do we best do this?

load_dotenv()

stage_name = os.environ.get("STAGE")

application_config = stage_list[stage_name]()
app = create_app(application_config)


login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)



def main(app):
    app.run()


if __name__ == "__main__":
    main(app)
