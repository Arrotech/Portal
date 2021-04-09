!['PythonVersion''](https://img.shields.io/badge/python-3.8.5-green.svg) [![Build Status](https://travis-ci.com/Arrotech/Portal.svg?branch=develop)](https://travis-ci.com/Arrotech/Portal) [![Coverage Status](https://coveralls.io/repos/github/Arrotech/Portal/badge.svg?branch=develop)](https://coveralls.io/github/Arrotech/Portal?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/d18f71e29c6588ba2043/maintainability)](https://codeclimate.com/github/Arrotech/Portal/maintainability) [![codecov](https://codecov.io/gh/Arrotech/Portal/branch/develop/graph/badge.svg?token=4s0xOjtFgH)](https://codecov.io/gh/Arrotech/Portal) [![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)] [![Codacy Badge](https://app.codacy.com/project/badge/Grade/5fee4cbf572043f3a5719e3e24262f91)](https://www.codacy.com/gh/Arrotech/Portal/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Arrotech/Portal&amp;utm_campaign=Badge_Grade) [![Known Vulnerabilities](https://snyk.io/test/github/Arrotech/Portal/badge.svg)](https://snyk.io/test/github/Arrotech/Portal)

**SCHOOL PORTAL**

This project is meant to Create a school portal with oython flask.

**TOOLS TO BE USED IN THE DEVELOPMENT**

1. Server-Side Framework: [Flask Python Framework](http://flask.pocoo.org/)
2. Linting Library: [Pylint, a Python Linting Library](https://www.pylint.org/)
3. Style Guide: [PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
4. Testing Framework: [PyTest, a Python Testing Framework](https://docs.pytest.org/en/latest/)
5. Testing Framework: [Coverage, a Python Testing Framework](https://coverage.readthedocs.io/en/v4.5.x/)

**REQUIREMENTS**

This are the basic project requirements. Make sure to install the before attempting to run the project.

    1. Python: [Install Python3](https://realpython.com/installing-python/)
    2. Postgres: [Install Postgres](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)
    3. Git: [Install Git](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-18-04)
    4. Node: [Install Node](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04)
    5. Postman: [Install Postman](https://linuxize.com/post/how-to-install-postman-on-ubuntu-18-04/)

The others can be downloaded and install from the requirements file. The installation process is outlined in the section `How to run the application`.

**HOW TO RUN THE APPLICATION**

Note that this project is meant for linux.

1.  Make a new directory on your computer and name it `portal` or give it any name of your choice.
2.  Navigate to the directory you have created and open it in the terminal.
3.  On the terminal type `git clone` and add this link <code>[repo](https://github.com/Arrotech/Portal/)</code> and the press `enter` to clone the remote repository to your local repository i.e `git clone 'link'`. Add the link without the quotation.
4.  Navigate to the directory that has been cloned to your machine and open it in a terminal.
5.  Create virtual environment by typing this in the terminal `virtualenv -p python3 venv`.
6.  Run `pip install -r requirements.txt` on the terminal to install the dependencies.
7.  Create `.env` file, copy the following environment variables and provide all the necessary information.

        source venv/bin/activate
        export FLASK_APP=run.py
        export FLASK_ENV=development
        export DEBUG_TB_INTERCEPT_REDIRECTS=False

        export REQUEST_STATS_WINDOW=15

        # database
        export DB_NAME=YOUR_DATABASE_NAME
        export TEST_DB_NAME=YOUR_TEST_DATABASE_NAME
        export DB_USER=YOUR_DATABASE_USERNAME
        export DB_HOST=YOUR_DATABASE_HOST
        export DB_PASSWORD=YOUR_DATABASE_PASSWORD

        # SQLALCHEMY
        export DATABASE_URL=YOUR_DATABASE_URI
        export TEST_DATABASE_URL=YOUR_TEST_DATABASE_URI
        export SQLALCHEMY_TRACK_MODIFICATIONS=False

        # brokers
        export LOCAL_RABBITMQ_URL=amqps://localhost//
        export RABBITMQ_URL=YOUR_HOSTED_RABBITQ_URL
        export LOCAL_REDISTOGO_URL=redis://
        export REDISTOGO_URL=YOUR_HOSTED_RABBITQ_URL

        # app secret key
        export SECRET_KEY=YOUR_APP_SECRET_KEY
        export JWT_SECRET_KEY=YOUR_JWT_SECRET_KEY

        # mail server
        export MAIL_SERVER=YOUR_MAIL_SERVER
        export MAIL_PORT=YOUR_MAIL_PORT
        export MAIL_USERNAME=YOUR_EMAIL
        export MAIL_PASSWORD=YOUR_EMAIL_PASSWORD
        export MAIL_USE_TLS=False
        export MAIL_USE_SSL=True

8.  Then type on the terminal `source .env` to activate the environment and also to export all the environment variables.
9.  Then type on the terminal `python3 manage.py runserver` to start and run the server.

**HOW TO RUN TESTS**

1.  Open a new terminal and then activate the environment.
2.  Type `python3 manage.py pytest` to run tests. This will run all tests and then give you a Coverage with details.

**OTHER IMPORTANT LINKS**

1.  Heroku deployment of the application: [Heroku](https://njc-school-portal.herokuapp.com/)
2.  Test coverage with coveralls: [Coveralls](https://coveralls.io/github/Arrotech/Portal)

**AUTHOR**

     Harun Gachanja Gitundu.
