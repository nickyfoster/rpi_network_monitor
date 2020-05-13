#syntax=docker/dockerfile:1.0.0-experimental
FROM python:3

WORKDIR /application
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY server ./server

WORKDIR /application/server
ENTRYPOINT [ "./boot.sh" ]
CMD ["4228", "4"]