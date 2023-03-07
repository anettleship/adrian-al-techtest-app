import os
from enum import Enum

class Config:

    """
    Primary class that implements default values common to all configurations, may be overwritten by children.
    """

    def __init__(self):
        # Default settings
        self.FLASK_ENV = os.environ.get("STAGE")
        self.DEBUG = False
        self.TESTING = False

        # Do not set a default secret key, we want application launch to fail by default if none set as part of application health checks
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.login_form_title = os.environ.get("LOGIN_FORM_TITLE")
        self.question_form_title = os.environ.get("QUESTION_FORM_TITLE")
        self.question_data_path = os.environ.get("QUESTION_DATA_PATH")


class Testing(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.TESTING = True


class Development(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.TESTING = True


class Production(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.FLASK_ENV = "production"
        self.TESTING = False 
