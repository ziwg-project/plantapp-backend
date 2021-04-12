FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
