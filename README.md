# adrian-al-techtest-app
Web application built for a job application tech test:

## Instructions to install and run on a local machine using the Flask inbuilt testing server:

Clone repository using git to local machine and navigate into this folder from the command line.

`git clone https://github.com/anettleship/adrian-al-techtest-app.git`

Install Python 3.11:
https://www.python.org/downloads/
Choose to add Python to Path

Verify this is installed python is installed by running `python` from a terminal session, it may be necessary to restart your terminal session or reboot your machine if you have never installed python before. 

Using your terminal, cd into the project folder adrian-al-testtest-app.

Install pipenv for python 3:
`pip3 install pipenv`

(On some platforms, this may need to be pip, rather than pip3).

You can Create a virtual environment for our project, with the correct version of python and download and install dependencies as listed in pipenv file:
`pipenv install`

We are using python 3.11.2, and this is specified in the pipenv Pipfile included with the project. If installed correct, this python version will be picked up by pipenv and used to make our virtual environment. If not, pipenv will throw an error, try reinstalling the correct python version, paying attention to the install location and adding it to your path. You may also need to reboot your machine.

Elevate our terminal so that our commands are executed in the contect of the virtual environment, with our project specific python version and dependencies:
`pipenv shell`

Make a note of the location of the virtual environment that's created. If you are using an IDE, you will need to configure your IDE to use the correct virtual environment. IDE specific instructions are outside this document's scope, for testing purposes we can use the terminal.

All python commands below must be run within a shell which has been elevated by running 'pipenv shell' first. Run `python` (on some systems this is `python3`).

We must now generate an app secret key (used to encrypt application data stored in the user's session cookie). Run the following commands sequentially within an interactive session by running and then copy the result to use in the next step:

`python`

`>>> import secrets`

`>>> secrets.token_urlsafe(16)`

`exit()`

Setting environment variables: Within the project structure is a folder named env_templates, it is necessary to copy the template.env file into the root of the project (place next to app.py) and rename it to .env. 

`cp env_templates/template.env .env`

Then manually insert the correct values for our application secret key: SECRET_KEY="" and the subscription key (included in requests to the external API that returns patient data from an NHS number, provided separately on request by the api owners): SUBSCRIPTION_KEY="" in between the quotes.

At this point, if you are deploying to production, change the variable STAGE from "development" to "production". This will cause our flask app to be loaded with debugging disabled.

We can verify the .env is being loaded successfully by running the following to view our secret key:

`python`

`>>> from dotenv import load_dotenv`

`>>> load_dotenv()`

`>>> import os`

`>>> os.environ.get("SECRET_KEY")`

`exit()`

Note, that my prefered choice for secrets such as secret keys and api keys would be a service like AWS Secrets Manager, as it solves the problem of how to deploy these secrets safely to other environments. For simplicity in this project, we place these secrets in our .env file manually when setting up the project. 

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

See file_structure.txt for an annotated list of folder heirarchies and the purpose of individual files.

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
