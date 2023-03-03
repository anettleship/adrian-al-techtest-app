# adrian-al-techtest-app
Web application built for a job application tech test

Install Python 3.11.2:
https://www.python.org/downloads/
Choose to add Python to Path

Install pipenv:
pip3 install pipenv

When creating the project I ran the following to create a virtual environment with the correct version of Python:
pipenv --python 3.11.2 

Now this version is written to our project's pipfile, you can Create a virtual environment for our project, with the correct version of python and download and install dependencies as listed in pipenv file:
pipenv install

If you really don't want to install another version of Python right now, you can modify the Pipfile python_version value to a version of Python you have installed, but I do not recommend this.

Elevate our terminal so that our commands are executed in the contect of the virtual environment, with our project specific python version and dependencies:
pipenv shell

Make a note of the name of the virtual environment that's created. If you are using an IDE, you will need to configure your IDE to use the correct virtual environment. IDE specific instructions are outside this document's scope, for testing purposes we can use the terminal, which doesn't depend on your choice of IDE.