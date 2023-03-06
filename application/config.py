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


class Testing(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.FLASK_ENV = "testing"
        self.TESTING = True


class Development(Config):
    """
    Config for instantiating an app within software tests.
    """

    def __init__(self):
        # initialise base class to inherit properties
        super().__init__()
        self.FLASK_ENV = "development"
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
