# DOCKERIZADO DEL FRONTEND
FROM node:20-alpine3.18 
WORKDIR .
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11.8-bullseye

# Set the working directory to /app
WORKDIR .
EXPOSE 8000
COPY . .
# Install system dependencies and update the package list
RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=backend.config.django.test
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000