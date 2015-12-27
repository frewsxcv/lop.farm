#!/bin/sh

# TODO: this file shouldn't exist. we should have multiple dockerfiles for each
#       environment. currently quay.io and docker hub don't make this easy
#       since they don't allow users to specify build context directories
#       or custom file names for dockerfiles

if [ "$1" = "web" ]; then
  cd $APP_DIR
  $PYTHON manage.py migrate
  $PYTHON manage.py runserver 0.0.0.0:8000
elif [ "$1" = "manage" ]; then
  shift
  cd $APP_DIR
  $PYTHON manage.py $*
elif [ "$1" = "worker" ]; then
  export C_FORCE_ROOT="true"
  $VENV_DIR/bin/celery -A lop_farm worker
elif [ "$1" = "test" ]; then
  cd $APP_DIR
  $PYTHON manage.py test
else
  echo "Invalid command"
  exit 1
fi;
