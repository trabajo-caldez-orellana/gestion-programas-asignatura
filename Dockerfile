FROM python:3.11.4

# Set the working directory to /home/app
EXPOSE 8000
# User without permissions
# RUN adduser --disabled-password --gecos '' celeryuser


# Install system dependencies and update the package list
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get install redis-server -y
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=backend.config.django.test
CMD python manage.py migrate && redis-server --daemonize yes && python manage.py runserver 0.0.0.0:8000