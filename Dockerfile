FROM python:3.12.0-slim

WORKDIR /django_app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update
RUN apt install -y libpq-dev gcc

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .