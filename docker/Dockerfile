FROM python:3.9.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install libpq-dev gcc

ARG CURRENT_UID=1000
RUN adduser --disabled-password --uid $CURRENT_UID --gecos "" app

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

RUN chown -R app /code/
USER app

RUN chmod +x /code/docker/docker-entrypoint.sh
ENTRYPOINT [ "/code/docker/docker-entrypoint.sh" ]