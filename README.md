# Image gallery

The image gallery enables users to search, browse, and view all our valuable imagery. Read [the product documentation](./docs/README.md) to understand the status of the product and what needs to be worked on.

## Development

The frontend application is written in React and uses hooks for state management.
The backend application is written in FastAPI and uses SQLite for data persistence.

### Installation

First, clone this repository.

#### Frontend

Change to the `frontend/` directory of the cloned repository. Then, install the dependencies using the following command:

```shell
$npm install
```

##### Running the application

This application uses Vite for fast building and hot module reloading. You can run the application using the following command:

```shell
$npm run dev
```

#### Backend

Change to the `backend/` directory of the cloned repository. Then, install the dependencies in a virtual environment using the following commands:

> [!WARNING]
>
> Please use Python 3.10 or above.

```shell
$ python --version
$ python -m venv .venv
$ source .venv/bin/activate
(.venv)$ python -m pip install .
$ Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

#### Running the application for backend

This project uses uvicorn to run the FastAPI application. You can run the application using the following command:

### shell

(.venv)$ uvicorn main:app --host 0.0.0.0 --port 9000 --reload

### commands

$pip install pytest requests
$pytest .\tests\test_api.py $to test
$pip install -r requirements.txt

### Questions

- what is Swagger UI: http://127.0.0.1:9000/docs
- using Django or FastAPI as a backend it could be connected to a frontend without using templates? it could be connected to both?
- how to create requirements file and download all the dependencies inside it?
- while installing dependencies, should i be in env mode or not? or it doesn't matter

#### Info

#### from unittest.mock import patch

- is used to mock database connections so we don't need a real database for testing

### to run specefic tests

$pytest .\tests\test_services.py::test_update_image_not_found

## TO DO

- create an APP without searching or googling it(models, views, etc)
- create tests for each file
- connect the backend with the frontend
