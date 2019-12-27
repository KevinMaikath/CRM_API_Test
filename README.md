# CRM_API_Test
CRM Service - API using Django-REST-Framework

## Project Setup
This project has been developed using a virtual environment. In order to install all the dependencies needed for this project, run the following steps in your terminal:
- Install 'pip' if necessary.
- Install 'virtualenv' if necessary.
```Shell
pip install virtualenv
```
- In the projects root directory, create a new virtual environment.
```Shell
virtualenv venv
```
(The command above creates and initializes a virtual environment called 'venv')
- Inside 'venv', install the project dependencies.
```Shell
pip install -r requirements.txt
```

## Database Setup
This project currently uses a local sqlite3 database. In order to setup this database, follow the next steps:
- Create the file 'db.sqlite3' in the projects root directory.
- Initialize the database:
```Shell
python manage.py migrate
```
