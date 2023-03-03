import os
from enum import Enum

# don't use enum, just add each class to a dictionary and lookup from the environment variable


class Config:

    """
    Primary class that implements default values common to all configurations, may be overwritten by children.
    """

    def __init__(self):
        # Default settings
        self.FLASK_ENV = "production" # set default to be production, but read environment variable
        self.DEBUG = False
        self.TESTING = False

        # Do not set a default secret key, we want application launch to fail by default if none set as part of application health checks
        self.SECRET_KEY = os.getenv("SECRET_KEY")


        # Raise an error here instead
        if self.SECRET_KEY == None:
            print("No secret key set, app will quit.")


class Testing(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.FLASK_ENV = "testing"
        self.TESTING = True
        self.SECRET_KEY = "testing secret key only lets not put this in production"


class Development(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.FLASK_ENV = "development"
        self.TESTING = True
        self.SECRET_KEY = "testing secret key only lets not put this in production"


class Production(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.FLASK_ENV = "production"
        self.TESTING = False 


stage_list = {
    "production" : Production,
    "development" : Development,
    "testing" : Testing
}