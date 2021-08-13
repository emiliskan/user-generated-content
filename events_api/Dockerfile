FROM python:3.9
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ARG POETRY_PARAMS="--no-dev"

RUN apt update && apt -y upgrade && apt install -y python3-setuptools netcat
RUN pip install pipenv

COPY ./Pipfile /opt/app/Pipfile

ENV PATH="${PATH}:/root/.local/bin"

RUN pipenv install --system --deploy --skip-lock

RUN mkdir /app
WORKDIR /app/
COPY / /app/
