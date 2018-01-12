#! /bin/bash

python3 manage.py migrate --settings=django_template.settings.base
python3 manage.py runserver --settings=django_template.settings.base 0.0.0.0:8000
