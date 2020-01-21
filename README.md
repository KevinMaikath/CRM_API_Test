# CRM_API_Test
CRM Service - API using Django-REST-Framework

## Getting started
Everything you need to know to run this API is explained in this README. However, for an initial set-up and run, it is 
recommended follow this section order:
1. [Install project's dependencies](#dependencies)
2. Connect the API to your database. You can use the default [sqlite3 file](#database-set-up) or a larger 
[MySQL database](#mysql-migration).
3. [Create the first user (superuser)](#superuser-creation).
4. [Set a default user image](#image-upload-settings).

Now the API should be ready to run. Check the [API Usage](#api-usage) for more details.

## Project set-up

### Dependencies
This project has been developed using a virtual environment. In order to install all the dependencies needed for this 
project, run the following steps in your terminal:
1. Install 'pip' if necessary.
2. Install 'virtualenv' if necessary.
```Shell
pip install virtualenv
```
3. Inside the project's root directory, create a new virtual environment.
```Shell
virtualenv venv
```
(The command above creates and initializes a virtual environment called 'venv')

4. Inside 'venv', install the project dependencies.
```Shell
pip install -r requirements.txt
```

### Database set-up
This project initially uses a local sqlite3 database. In order to setup this database, follow the next steps:
1. Create the file 'db.sqlite3' in the project's root directory.
2. Initialize the database:
```Shell
python manage.py migrate
```

### MySQL migration
The sqlite3 database is suitable and can store a good amount of data for small projects. However, for bigger projects, 
you can make use of a larger, remote database like MySQL. In order to set-up this API for MySQL, just follow the next steps:
1. Install 'mysqlclient'.
```Shell
pip install mysqlclient
```

2. Configure the project's settings. Inside 'KevinMaikath_CRM_API_Test/settings.py' you have the initial database 
settings:
```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
Change it to the following:
```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<DATABASE_NAME>',
        'USER': '<YOUR_USER>',
        'PASSWORD': '<YOUR_PASSWORD>',
        'HOST': '<MYSQL_SERVER_IP>',
        'PORT': '<MYSQL_SERVER_PORT>',
    }
}
```

### Image upload settings
Image upload settings are located at 'KevinMaikath_CRM_API_Test/settings.py'. The initial values are the following:
```Python
IMAGE_FOLDER = 'images/'
IMAGE_FORMAT = 'png'
IMAGE_MAX_HEIGHT = 300
IMAGE_MAX_WIDTH = 300
DEFAULT_IMAGE_FILE = 'default.png'
```

As the image field is optional for customer creation, it is necessary to manually store a default image in the images 
folder ('media/images/' by default). This way, every new user without image will take the default one.

## API Usage
To run the API project:
```Shell
python manage.py runserver
```


### Authentication
This API uses token authentication. To get the token from an exiting user:
1. Send a POST request to '/auth/login', providing the username and the password. If the login is successful, it will return 
the corresponding token.
2. Use this token for authentication in every other request. Set it as an HTTP Header called 'Authorization', and the 
token in the value field. For example, for a given token '1234', the header would be the following:
```
'Authorization': 'Token 1234'
```

The token expiry time is given by a settings variable. It has a default value of 60 seconds, but you can change it in 
'settings.py'.

### Superuser creation
Creating a superuser is always needed to start using the API, as the database might be initially empty and you will 
probably need to create other users.

In order to create a new superuser, send a POST request to '/auth/admin' with an email, username and password.

**For the first superuser**, you will not need to be authenticated to create it, but you will need to be authenticated
as a superuser to create others from now on.


### User creation
To create a new user, send a POST request to '/auth/users', specifying the username, email and password. You need to be 
authenticated for this action, and **only superusers can create other users**.

The password will be stored as a hash value for security. The username can't be repeated in the database. 
An authorization token will be automatically provided to the user when created.


### Currently available requests
This API uses Swagger (OpenAPI) for its documentation.
You can get all the available API paths in different ways, sending a GET request to:

- '/swagger': show the default Swagger UI.
- '/swagger.json': return the Swagger-generated docs as a JSON file.
- '/swagger.yaml': return the Swagger-generated docs as a YAML file.
- '/redoc': show a summarized documentation of the API's paths.

### Image uploads
Whenever customer with an image is created, the image will be stored in the project's image folder 
(configured in 'settings.py'). If no image is set when creating a customer, it will automatically get the default one.

In order to decrease the image storage capacity, every uploaded image will be cropped if it doesn't fit the maximum 
configured size. Moreover, when a customer's image is updated, the previous image will be removed from the images 
folder.


## Project testing
To run all the project's tests, simply run the next command:
```Shell
python manage.py test
```

## Docker build
In order to build the project and run it as a Docker container, follow the next steps:
1. Build the Docker image:
```Shell
docker-compose build
```

2. Connect and migrate to the database (creates an sqlite3 file if it doesn't exist):
```Shell
docker-compose run web python manage.py migrate
```

3. Run the Docker image:
```Shell
docker-compose up
```