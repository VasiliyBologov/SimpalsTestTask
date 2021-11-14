

# Guid to TestTask:

Step 1(done). Download all ads from Johny194 account, send data in json format in response to a request to your API
Step 2(done). Download all ads from Johny194 account, save MongoDB data.
Step 3(done). All prices on ads, before saving, which are indicated in EUR convert to MDL at today's rate.
Step 4(done). Set up ad change tracking for your Johny194 account and contribute them to MongoDB.
Step 5(done). Synchronize data from MongoDB with Elasticsearch.

## Note for Step 5: 
There is no point in reinventing the wheel and inventing the synchronization of MongoDB and Elasticsearch.  
There is a wonderful thing like [mongo-connector](https://github.com/yougov/mongo-connector), but unfortunately it works up to version 3.6.  
Therefore, it is more relevant to take the written in Goleng [Monstache](https://github.com/rwynn/monstache)

# Monstache

How run that servise [here](https://rwynn.github.io/monstache-site/start/)

## Elasticsearch

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

# Poetry

Poetry (https://python-poetry.org/) is used to manage app dependencies. You install it globally

    pip3 install poetry


Install the dependencies:

    poetry install # add --no-dev for production

To activate the virtual environment (which is automatically created in `.venv` during `poetry install`):

    . .venv/bin/activate


Run the development server which automatically reloads when it detects changes in the code:

    ./main.py dev-server

To update versions of dependencies:

    poetry update


# Settings
    
Configuration options are defined in `conf.py` for different environment types. Environment
type is defined by `ENVIRONMENT` option, which is usually set by the corresponding environment
variable.

You can also create file `.env` in the project root folder. This git ignored file contains custom 
settings which are overrideable via environment variables.

See also https://pydantic-docs.helpmanual.io/usage/settings/#parsing-environment-variable-values


# Run the web app in a Docker container

    # Build the image
    docker build -t simpals-test-task . -f docker/app.Dockerfile

    # Run the image
    docker run -it --rm --name=simpals_test_task -p 80:80 simpals-test-task 

    # Passing env vars 
    docker run -it --rm --name=simpals_test_task -p 80:80 --env ENVIRONMENT=dev simpals-test-task

    # Run bash inside the container if needed, using the name 
    docker exec -it simpals_test_task /bin/bash


# API docs

The API docs are available at `/docs`. They are password protected in staging environment and disabled
on prod.


# FastAPI

We are using sync code in async functions. See https://github.com/tiangolo/fastapi/issues/260#issuecomment-495945630