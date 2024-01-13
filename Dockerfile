#!/usr/bin/env ./.build.sh
FROM python:3.12-alpine

ADD . /app
WORKDIR /app

RUN apk add git
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
