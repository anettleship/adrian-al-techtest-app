# adrian-al-techtest-app
Web application built for a job application tech test:

## Instructions to install and run on a local machine using the Flask inbuilt testing server:

Clone repository using git to local machine and navigate into this folder from the command line.
`git clone https://github.com/anettleship/adrian-al-techtest-app.git`

Install Python 3.11.2:
https://www.python.org/downloads/
Choose to add Python to Path

Verify this is installed python is installed by running `python` from a terminal session, it may be necessary to restart your terminal session or reboot your machine if you have never installed python before. 

Install pipenv for python 3:
`pip3 install pipenv`

(On some platforms, this may need to be pip, rather than pip3).

You can Create a virtual environment for our project, with the correct version of python and download and install dependencies as listed in pipenv file:
`pipenv install`

We are using python 3.11.2, and this is specified in the pipenv Pipfile included with the project. If installed correct, this python version will be picked up by pipenv and used to make our virtual environment. If not, pipenv will throw an error, try reinstalling the correct python version, paying attention to the install location and adding it to your path. You may also need to reboot your machine.

Elevate our terminal so that our commands are executed in the contect of the virtual environment, with our project specific python version and dependencies:
`pipenv shell`

Make a note of the name of the virtual environment that's created. If you are using an IDE, you will need to configure your IDE to use the correct virtual environment. IDE specific instructions are outside this document's scope, for testing purposes we can use the terminal.

All python commands below must be run within a shell which has been elevated by running 'pipenv shell' first. Run `python` (on some systems this is `python3`).

We must now generate an app secret key (used to encrypt application data stored in the user's session cookie). Run the following commands sequentially within an interactive session by running and then copy the result to use in the next step:

`python`
`>>> import secrets`
`>>> secrets.token_urlsafe(16)`

Setting environment variables: Within the project structure is a folder named env_templates, it is necessary to copy the template.env file into the root of the project (place next to app.py) and rename it to .env. Then manually insert the correct values for our application secret key: SECRET_KEY="" and the subscription key (included in requests to the external API that returns patient data from an NHS number, provided separately on request by the api owners): SUBSCRIPTION_KEY="" in between the quotes.

We can verify the .env is being loaded successfully by running the following to view our secret key:

`python`
`>>> from dotenv import load_dotenv`
`>>> load_dotenv()`
`>>> os.environ.get("SECRET_KEY")`

Note, that my prefered choice for secrets such as secret keys and api keys would be a service like AWS Secrets Manager. For simplicity in this project, we place these secrets in our .env file manually when setting up the project. 

Production deployment is outside the scope of this document, but note that it will be necessary to ensure these environment values are set on any machine which runs our service.

Now we have set up our environment variables, still running within our virtual environment terminal, at the root of our project directory, elevated by running pipenv shell earlier, we can run the following to run our tests:

`pytest`

If all tests pass, we can then run the following to start our server. Note the web address where this is being served and navigate to this URL from a web browser, to access our application:

`flask run`

## High Level Design:

This is a Flask application implemented with an app_factory to instantiate apps with different settings for testing, development and production. It is implemented with a single blueprint, to keep the application itself separate from the component: t2lifestylechecker that addresses our requirements.

We use pipenv for virtual environment management, python-dotenv for environment variables management from a .env file, pytest for testing and requests to call our external api.  For frontend we use bootstrap to simplify css layout. 

I chose Flask in favour of Django because it results in a ligher weight codebase, can be stood up faster, and because the requirements ask for a simple application and do not specify the need for a database.

We're using pytest-recording to 'playback' api responses from the external api for our tests rather than testing against the live external api.

When adding or changing tests with the @pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"])) decorator, it is necessary to run the following command to place a live request to the external api and record the result for any tests which do not have a matching 'recording' in the tests/cassettes folder. These are provided in the package, so the following command is not necessary in order to run tests if no changes are made to them.

pytest --record-mode=once

We have pytest-cov in the requirements to check test coverage, including branch coverage. This is not set up to run automatically, as this would slow down running our tests. This can be run manually by the following command with a shell elevated to the virtual environment.

pytest --cov

## File Structure


`adrian-al-techtest-app
|
|   .env - stores locally configured environment variables, not committed to source control, copy template.env to make your own.
|   .gitignore - specifies files which git should ignore, such as .env 
|   app.py - the start point of our flask app, run this to run the flask application locally
|   Pipfile - used by pipenv, lists dependencies.
|   Pipfile.lock - used by pipenv
|   README.md - read this first
|   requirements.txt - lists all module versions
|   setup.cfg - used to configure pytest-cov to look at branch coverage
|   
+---application - files related to standing up our flask application and loading the t2lifestylechecker blueprint
|       app_factory.py - code that deals with standing up our flask application
|       auth.py - code that handles setting up our login manager for authentication
|       config.py - holds a class used to configure our flask application
|       config_stages.py - holds an enum that defines valid settings for our stage variable in .env - determines actions when Config class is initialised
|       __init__.py - helps python to discover modules in this folder
|           
+---env_templates
|       template.env - template environment variables, readme describes how to copy this to create your own .env file.
|       
+---t2lifestylechecker - all functionality related to requirements for t2lifestylechecker located here, defines a blueprint for re-use in other applications
    |   external_validation_handler.py - class to handle login function of first form (part 1)
    |   external_validation_handler_helper.py - helper functions for above class, holds a dictionary of localised messages to show user, indexed by language code
    |   questionnaire_handler.py - class to handle questionnaire function of the second form (part 2)
    |   t2lifestylechecker.py - all routes for application blueprint are defined here
    |   t2lifestylechecker_config.py - holds enums that define valid responses and states for objects and interactions in our project
    |   __init__.py - helps python to discover modules in this folder
    |   
    +---question_data
    |       default_question_data.json - represents questions, answers, age range thresholds and points for our questionnaire - demonstates how language locallisation could be built out if required
    |       test_invalid_question_data.json - an intentionally invalid json file for testing basic data validation (part 3)
    |       
    +---static
    |   \---js
    |           testfile.js - our frontend uses Content Delivery Network links for css and js files, this route could accomodate serving static files if required
    |           
    +---templates
    |       base.html - base html jinja template extended by all other templates
    |       login.html - template for login page form
    |       message.html - template to return user messages after login and questionnaire form entry
    |       questionnaire.html - template for questionnaire page form
    |       
    +---tests - acceptance tests for the corresponding modules of for test_module_name
        |   test_external_validation_handler.py 
        |   test_external_validation_handler_helper.py 
        |   test_questionnaire_handler.py
        |   test_t2lifestylechecker.py
        |   __init__.py - helps python to discover modules in this foldery
        |   
        +---cassettes - contains yaml files recording api responses for tests managed by pytest-record`
        


## Design Notes

Localisation

There's a minor ambiguity in the specifications, as the age ranges for different points for answers to our questionnaire run 41-65 and then 64+, so that the ranges overlap. I have assumed this should be 41-64 and then 65+; the questionnaire and thresholds are loaded from a static json file, which can be edited if these values require adjustment.

Validity checking:


# cannot load json
# cannot parse json
# any answer points length does not match age range maximums list + 1

# no min age
# min age not int
# no age range maximums set
# age range maximums not int
# age range maxiumums not sorted low to high
# no questions property set
# questions length is 0
# question missing any of name, text, answers, and check if any fields length is 0
# length of message maximums needs to be one less than length of messages list
# json trailing commas
# messages['states'] and dictionaries for each language match

Build this out into a web form with validation, and the ability for a user to input sample answers and sense check the results are as expected.

Language should be a user property to allow users to switch between languages.
