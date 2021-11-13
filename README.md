# Poetry

Poetry (https://python-poetry.org/) is used to manage app dependencies. You install it globally

    pip3 install poetry


Install the dependencies:

    poetry install # add --no-dev for production

To activate the virtual environment (which is automatically created in `.venv` during `poetry install`):

    . .venv/bin/activate

Create an admin user:

    ./manage.py create-superuser

Run the development server which automatically reloads when it detects changes in the code:

    ./manage.py dev-server

To update versions of dependencies:

    poetry update


# Run tests

    ./manage.py test

After the tests are run, code coverage files are created in `var/coverage/` directory.
You can open `var/coverage/index.html` to see HTML formatted coverage stats.
`coverage.xml` holds coverage report in XML format.


# Settings
    
Configuration options are defined in `config.py` for different environment types. Environment
type is defined by `ENVIRONMENT` option, which is usually set by the corresponding environment
variable.

You can also create file `.env` in the project root folder. This git ignored file contains custom 
settings which are overrideable via environment variables.

See also https://pydantic-docs.helpmanual.io/usage/settings/#parsing-environment-variable-values


# Run the web app in a Docker container

    # Build the image
    docker build -t client-portal . -f docker/app.Dockerfile

    # Run the image
    docker run -it --rm --name=client_portal -p 80:80 client-portal

    # Passing env vars 
    docker run -it --rm --name=client_portal -p 80:80 --env ENVIRONMENT=staging client-portal

    # Run bash inside the container if needed, using the name 
    docker exec -it client_portal /bin/bash


# API docs

The API docs are available at `/docs`. They are password protected in staging environment and disabled
on prod.


# FastAPI

We are using sync code in async functions. See https://github.com/tiangolo/fastapi/issues/260#issuecomment-495945630

