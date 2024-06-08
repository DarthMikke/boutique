#!/bin/bash

if [ -z $VENV ]; then
VENV="/app/venv"
fi

if [ -z $APP_DIR ]; then
APP_DIR="/app"
fi

if [ -z $ASGI_APPLICATION ]; then
ASGI_APPLICATION="asgi:application"
fi

echo Configuration:
echo VENV: $VENV
echo APP_DIR: $APP_DIR
echo ASGI_APPLICATION: $ASGI_APPLICATION

echo "Activating venv..."
python3 -m venv $VENV
source $VENV/bin/activate

cd $APP_DIR

# Scenarios:
# 1. Run fastwsgi
if [ $1 == "production" ]; then
  fastwsgi -a $ASGI_APPLICATION $?
  exit $?
elif [ $1 == "install" ]; then
  pip install -r requirements.txt
  exit $?
fi

pip install -r requirements.txt

# Pass arguments to manage.py
set -x
python3 manage.py $@
