#!/bin/bash

# Realizar migraciones
python manage.py migrate

# Instalar dependencias externas!
apt-get weasyprint

# Iniciar el servidor
python manage.py runserver 0.0.0.0:8000