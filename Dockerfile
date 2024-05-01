FROM python:3.11.8-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
# Copiar el script de inicio
RUN chmod +x ./start.sh;
EXPOSE 8000

# Ejecutar el script de inicio
ENTRYPOINT ["sh", "./start.sh"] 