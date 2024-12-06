FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.8.0/dockerize-alpine-linux-amd64-v0.8.0.tar.gz -o /tmp/dockerize.tar.gz && \
    tar -xvf /tmp/dockerize.tar.gz -C /usr/local/bin && \
    rm /tmp/dockerize.tar.gz


RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

