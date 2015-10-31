FROM ubuntu:15.10

# Django app directory
ENV APP_DIR /srv/app

# virtual environment directory
ENV VENV_DIR /srv/venv

# virtual environment pip path
ENV PIP $VENV_DIR/bin/pip

# virtual environment Python path
ENV PYTHON $VENV_DIR/bin/python

ADD . $APP_DIR
WORKDIR $APP_DIR

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y python3 python3-venv
RUN python3 -m venv $VENV_DIR
RUN $PIP install -r requirements.txt

ENTRYPOINT ["/srv/venv/bin/python", "/srv/app/manage.py", "runserver"]
