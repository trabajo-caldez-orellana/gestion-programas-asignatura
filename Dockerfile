# DOCKERIZADO DEL FRONTEND
FROM node:20-alpine3.18 
RUN mkdir /app
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install
COPY . /app/
CMD ["npm", "run", "build"]


FROM python:3.11.8-bullseye

# Set the working directory to /app
WORKDIR /app
EXPOSE 8000
COPY . /app/
# Install system dependencies and update the package list
RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000