#! /bin/bash

python manage.py migrate --settings=django_template.settings.base
python manage.py runserver --settings=django_template.settings.base 0.0.0.0:8000
