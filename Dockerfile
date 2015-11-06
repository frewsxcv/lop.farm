FROM ubuntu:15.10

# Django app directory
ENV APP_DIR /srv/app

# virtual environment directory
ENV VENV_DIR /srv/venv

# virtual environment pip path
ENV PIP $VENV_DIR/bin/pip

# virtual environment Python path
ENV PYTHON $VENV_DIR/bin/python

RUN apt-get update && apt-get install -y \
  gcc \
  libffi-dev \
  make \
  libssl-dev \
  python3 \
  python3-dev \
  python3-venv \
  wget

# Install AFL
WORKDIR /tmp/afl
RUN wget http://lcamtuf.coredump.cx/afl/releases/afl-1.94b.tgz
RUN tar -xf afl-1.94b.tgz
WORKDIR /tmp/afl/afl-1.94b
RUN make
RUN make install

ADD . $APP_DIR
WORKDIR $APP_DIR

RUN python3 -m venv $VENV_DIR
RUN $PIP install --upgrade pip
RUN $PIP install cython
RUN $PIP install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/srv/venv/bin/python", "/srv/app/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
