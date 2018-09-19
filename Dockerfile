FROM python:3.6-alpine3.8

RUN pip install selenium requests pyyaml

ENV TZ Australia/Sydney

RUN mkdir /app

WORKDIR /app

COPY . /app