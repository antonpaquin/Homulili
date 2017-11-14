#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/backend.pid"
SRCDIR=$DOCROOT/src/manga_host/flask
SRCFILE=route.py

source process_ctl.sh
