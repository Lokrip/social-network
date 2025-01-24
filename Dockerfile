FROM python:latest

WORKDIR /service
COPY requirements.txt /temp/requirements.txt
COPY . /service

RUN apt-get update && apt-get install -y postgresql-client build-essential libpq-dev
RUN apt update && apt install -y iproute2
RUN apt update && apt install -y net-tools

EXPOSE 8000

RUN pip install -r /temp/requirements.txt
