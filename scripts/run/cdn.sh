#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/cdn.pid"
SRCDIR=$DOCROOT/src/cdn/flask
SRCFILE=route.py

source process_ctl.sh
