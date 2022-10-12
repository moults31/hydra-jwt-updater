# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY hydra .
COPY update-jwt.py .

CMD [ "python3", "-u", "update-jwt.py"]