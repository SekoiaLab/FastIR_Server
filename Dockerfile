FROM ubuntu:xenial
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-flask python3-psycopg2 python3-flask-sqlalchemy python3-click openssl
RUN useradd -d /code foo
ADD . /code
RUN chown -R foo. /code
WORKDIR /code
USER foo
CMD ./start.py
