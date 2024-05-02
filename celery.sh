#!/bin/bash

# Realizar migraciones
python manage.py migrate

exec "$@"