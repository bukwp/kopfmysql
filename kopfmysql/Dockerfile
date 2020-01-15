FROM python:3-slim

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code
ENTRYPOINT ["kopf", "run", "handlers.py"]
