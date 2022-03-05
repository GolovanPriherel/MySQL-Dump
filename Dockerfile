# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src /src
COPY ./data /data
COPY main.py main.py

CMD [ "python3", "main.py" ]