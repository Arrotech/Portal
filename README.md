[![Build Status](https://travis-ci.org/Arrotech/Portal.svg?branch=develop)](https://travis-ci.org/Arrotech/Portal) [![Coverage Status](https://coveralls.io/repos/github/Arrotech/Portal/badge.svg?branch=bg-remove-coveralls-badge-167397034)](https://coveralls.io/github/Arrotech/Portal?branch=bg-remove-coveralls-badge-167397034) [![Maintainability](https://api.codeclimate.com/v1/badges/d18f71e29c6588ba2043/maintainability)](https://codeclimate.com/github/Arrotech/Portal/maintainability) [![codecov](https://codecov.io/gh/Arrotech/Portal/branch/gh-pages/graph/badge.svg)](https://codecov.io/gh/Arrotech/Portal) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


**SCHOOL PORTAL**

This project is meant to Create a school portal with Python, Flask, HTML, Node, CSS and JavaScript. The project is built on Linux.

Below are the Endpoints that have been created.

| EndPoints       | Functionality  | HTTP Method  |
| ------------- |:-------------:| -----:|
| /api/v1/auth/register | Create user| POST |
| /api/v1/auth/login | Login to account |GET|
| /api/v1/exams |  Add Exams | POST |
| /api/v1/exams | Fetch all Exams | GET |
| /api/v1/exams/admission_no | Fetch one Exam | GET |
| /api/v1/exams/admission_no | Edit an Exam | PUT |
| /api/v1/exams/admission_no | Delete an Exam | DELETE |
| /api/v1/users/admission_no | Fetch a specific user | GET |
| /api/v1/fees |  Add Fees | POST |
| /api/v1/fees | Fetch all Fees | GET |
| /api/v1/fees/admission_no | Fetch Specific Fee | GET |
| /api/v1/books |  Add Books | POST |
| /api/v1/books | Fetch all Books | GET |
| /api/v1/books/admission_no | Fetch Specific Book | GET |
| /api/v1/id |  Add Student Information | POST |
| /api/v1/id | Fetch Students Information | GET |
| /api/v1/id/admission_no | Fetch Specific Student Information | GET |
| /api/v1/subjects |  Register Subjects | POST |
| /api/v1/subjects | Fetch all Subjects | GET |
| /api/v1/subjects/admission_no | Fetch Specific Subject | GET |


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

 1. Make a new directory on your computer and name it `portal` or give it any name of your choice.
 2. Navigate to the directory you have created and open it in the terminal.
 3. On the terminal type `git clone` and add this link <code>[repo](https://github.com/Arrotech/Portal/)</code> and the press `enter` to clone the remote repository to your local repository i.e `git clone 'link'`. Add the link without the quotation.
 4. Navigate to the directory that has been cloned to your machine and open it in a terminal.
 5. Create virtual environment by typing this in the terminal `virtualenv -p python3 venv`.
 6. Run `pip install -r requirements.txt` on the terminal to install the dependencies.
 7. Then type on the terminal `source .env` to activate the environment and also to export all the environment variables.
 8. Then type on the terminal `flask run` to start and run the server.
 9. To run the HTML pages, make sure you have node already installed in your machine. Click [Here](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) and follow the process to install node.
 10. Open another terminal and make sure the environment is activate. If not type `source .env` to activate it.
 11. The type `live-server` to run the pages locally.
 12. You can now interact with the project.


**HOW TO RUN TESTS**

 1. Open a new terminal and then activate the environment.
 2. Type `pytest --cov=app --cov-report=term-missing` and hit `enter`. This will run all tests and then give you a Coverage with details.

 **OTHER IMPORTANT LINKS**

 1. Heroku deployment of the application: [Heroku](https://arrotech-school-portal.herokuapp.com/)
 2. Test coverage with coveralls: [Coveralls](https://coveralls.io/github/Arrotech/Portal)


**AUTHOR**

     Harun Gachanja Gitundu.
