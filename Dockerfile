# DOCKERIZADO DEL FRONTEND
FROM node:20-alpine3.18 
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11.8-bullseye
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
# Copiar el script de inicio
RUN chmod +x ./start.sh;
EXPOSE 8000
# Ejecutar el script de inicio
ENTRYPOINT ["sh", "./start.sh"]
