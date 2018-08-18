#!/bin/bash
./manage.py makemigrations
./manage.py migrate
python3 manage.py migrate --run-syncdb
