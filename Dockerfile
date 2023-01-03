FROM python:3.8.3-slim
ENV PYTHONUNBUFFERED 1


WORKDIR /core
# RUN apt-get build-dep python-psycopg2

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:80
