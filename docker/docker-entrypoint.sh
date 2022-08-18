#!/bin/bash

case "$1" in

runserver)
  shift
  python manage.py migrate
  python manage.py runserver 0.0.0.0:8001
  ;;

test)
  shift
  exec pytest "$@"
  ;;

esac