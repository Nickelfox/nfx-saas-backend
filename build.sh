#!/bin/bash
#activate the virtual environment

source ./venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

##
python manage.py collectstatic --noinput
