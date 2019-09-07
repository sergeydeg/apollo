FROM python:3.6-slim-buster

RUN apt-get update \
  && apt-get -y install build-essential \
  && apt-get -y install default-mysql-server \
  && apt-get -y install default-libmysqlclient-dev \
  && apt-get -y install python-dev \
  && pip install alembic \
  && pip install pipenv

WORKDIR /apollo

COPY Pipfile Pipfile.lock ./
RUN pipenv install

ADD . /apollo

CMD pipenv run python ./app.py
