# CRM_API_Test
CRM Service - API using Django-REST-Framework

## Project set-up

### Dependencies
This project has been developed using a virtual environment. In order to install all the dependencies needed for this project, run the following steps in your terminal:
1. Install 'pip' if necessary.
2. Install 'virtualenv' if necessary.
```Shell
pip install virtualenv
```
3. In the projects root directory, create a new virtual environment.
```Shell
virtualenv venv
```
(The command above creates and initializes a virtual environment called 'venv')
4. Inside 'venv', install the project dependencies.
```Shell
pip install -r requirements.txt
```

### Database set-up
This project currently uses a local sqlite3 database. In order to setup this database, follow the next steps:
1. Create the file 'db.sqlite3' in the projects root directory.
2. Initialize the database:
```Shell
python manage.py migrate
```

## API Usage
To run the API project:
```Shell
python manage.py runserver
```


#### Authentication
This API uses token authentication. To get the token of an exiting user:
1. Send a POST request to '\login', providing the username and the password. If the login is successful, it will return the corresponding token.
2. Use this token for authentication in every other request. Set it as an HTTP Header called 'Authorization', and the token in the value field. For example, for a given token '1234', the header would be the following:
```
'Authorization': 'Token 1234'
```


#### User creation
To create a new user, send a POST request to '\users', specifying the username, email and password. No authorization is needed for this request.

The password will be stored as a hash value for security. The username can't be repeated in the database. An authorization token will be automatically provided to the user when created.


#### Currently available requests
These are all the available requests to get and manipulate the customers data. Token authorization is needed for all of them.

- '/customers'
  - GET: returns a list with all the customers.
  - POST: creates a customer instance into the database. Required parameters:
      - name: customers name.
      - surname: customers surname.
      - imgUrl: URL for the customers image.
      
'imgUrl' field is optional. If it isn't set in the request, it will get the default value 'No image yet'.
      
- '/customer/{customerID}'
  - PUT: updates the specified customer. All parameters are optional.
  - DELETE: deletes the specified customer.
