FROM python:3-slim

RUN apt-get update && apt-get upgrade
RUN apt-get install wait-for-it

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY /app /app
ENTRYPOINT ["kopf", "run", "main.py"]
