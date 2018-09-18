FROM python:3.6-alpine3.8

RUN pip install selenium requests pyyaml

RUN mkdir /app

WORKDIR /app

COPY . /app