#!/bin/bash

# Realizar migraciones
python manage.py migrate

# Instalar dependencias externas!
apt-get weasyprint

exec "$@"