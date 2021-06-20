FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app
COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN celery -A plantapp worker -l info --concurrency 1 -P solo &
RUN celery -A plantapp beat -l info -S django &