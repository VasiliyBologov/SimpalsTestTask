#!/bin/sh

echo 'Starting Nginx'
service nginx start

echo 'Starting the backend'
poetry run ./main.py start-supervisor
