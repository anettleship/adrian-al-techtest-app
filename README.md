# adrian-al-techtest-app
Web application built for a job application tech test.

High Level Design:

This is a Flask application implemented with an app_factory to instantiate apps with different settings for testing, development and production. It is implemented with a single blueprint, to keep the application itself separate from the component: t2lifestylechecker that addresses our requirements.

We use pipenv for virtual environment management, pytest for testing and requests to call our external api.

I chose Flask in favour of Django because it results in a ligher weight codebase, can be stood up faster, and because the requirements do not specify the need for a database and ask for a simple application.

For frontend we use bootstrap and a small amount of jQuery to provide better user experience while we are calling our external api. - maybe this part will be a nice to have, along with Asyncronouse call to the api.

We allow single digit input for day and month (although the interface requests 2), but we only accept 4 digit input for years, to avoid ambiguity between 2023 and 1923 - mention how I would add better error checking and user feedback on invalid input for invalid dates.

We're using pytest-recording to 'playback' api responses from the external api for our tests.

When adding or changing tests with the @pytest.mark.vcr(filter_headers=(["Ocp-Apim-Subscription-Key"])) decorator, it is necessary to run the following command to place a live request to the external api and record the result for any tests which do not have a matching 'recording' in the tests/cassettes folder. These are provided in the package, so the following command is not necessary in order to run tests if no changes are made to them.

pytest --record-mode=once

Note: the external api does not return consistent date of birth for the same nhsnumber. We validate
user input using age rather than exact date of birth as a result, and tests use a 'pre-recorded' response using pytest-recording, but might fail erroneously if that response is 're-recorded'.

That is not true, the external api provides a consistent date of birth but varies the year to preserve age in the requirements for each individual as time passes. One item to be addressed is to use the requirements age as an input for the tests, so the age in the requirements is tracked by the tests - otherwise within a years time, all our tests will need to have their date of birth years incremented.

Mention test coverage

Scoring, specifications are ambiguous, I went with 41-64 and then 65+

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


Instructions to install and run on a local machine using the Flask inbuilt testing server:

Install Python 3.11.2:
https://www.python.org/downloads/
Choose to add Python to Path

Install pipenv:
pip3 install pipenv

When creating the project I ran the following to create a virtual environment with the correct version of Python:
pipenv --python 3.11.2 

Certainly newer than Python 3.6

Now this version is written to our project's pipfile, you can Create a virtual environment for our project, with the correct version of python and download and install dependencies as listed in pipenv file:
pipenv install

If you really don't want to install another version of Python right now, you can modify the Pipfile python_version value to a version of Python you have installed, but I do not recommend this.

Elevate our terminal so that our commands are executed in the contect of the virtual environment, with our project specific python version and dependencies:
pipenv shell

Make a note of the name of the virtual environment that's created. If you are using an IDE, you will need to configure your IDE to use the correct virtual environment. IDE specific instructions are outside this document's scope, for testing purposes we can use the terminal, which doesn't depend on your choice of IDE

Instructions for environment variables and adding the required information to our sample .env file.

Mention deployment, how we might serve static files more efficiently outside flask and need to set environment variables and Flask secret key + how to generate secret key.
