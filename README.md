# adrian-al-techtest-app
Web application built for a job application tech test.

High Level Design:

This is a Flask application implemented with an app_factory to instantiate apps with different settings for testing, development and production. It is implemented with a single blueprint, to keep the application itself separate from the component: t2lifestylechecker that addresses our requirements.

I chose Flask in favour of Django because it results in a ligher weight codebase, can be stood up faster, and because the requirements do not specify the need for a database and ask for a simple application.

For frontend we use bootstrap and a small amount of jQuery to provide better user experience while we are calling our external api. - maybe this part will be a nice to have, along with Asyncronouse call to the api.

We allow single digit input for day and month (although the interface requests 2), but we only accept 4 digit input for years, to avoid ambiguity between 2023 and 1923 - mention how I would add better error checking and user feedback on invalid input for invalid dates.

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
