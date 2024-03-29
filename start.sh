#!/bin/bash

# Realizar migraciones
python manage.py migrate

# Iniciar el servidor
python manage.py runserver 0.0.0.0:8000