# pull official base image
FROM python:3.9-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install fastapi[all]
RUN pip install uvicorn
RUN pip install sqlmodel
RUN pip install python-telegram-bot --upgrade
RUN pip install psycopg2-binary

COPY . /code/