#!/bin/bash
#activate the virtual environment

source ./venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

#load Common app -> media fixture
python manage.py loaddata fixtures/media.json

#load User app -> user fixture
python manage.py loaddata fixtures/user.json

#load Project app fixtures
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/keywords.json
python manage.py loaddata fixtures/client.json
python manage.py loaddata fixtures/project.json
python manage.py loaddata fixtures/projectimages.json
python manage.py loaddata fixtures/clientsproject.json
python manage.py loaddata fixtures/websiteimage.json
python manage.py collectstatic --noinput
