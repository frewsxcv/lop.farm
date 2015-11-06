FROM ubuntu:15.10

# AFL direcotry
ENV AFL_DIR /srv/afl
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
ENV AFL_HARDEN 1
WORKDIR $AFL_DIR
RUN wget http://lcamtuf.coredump.cx/afl/releases/afl-1.94b.tgz
RUN tar --strip-components=1 -xf afl-1.94b.tgz
RUN make
RUN make install

RUN python3 -m venv $VENV_DIR
ENV PATH $PATH:$VENV_DIR/bin/

RUN $PIP install cython

ADD . $APP_DIR
WORKDIR $APP_DIR

RUN $PIP install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/srv/venv/bin/python", "/srv/app/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
