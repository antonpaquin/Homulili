#! /bin/bash

DOCROOT="$(pwd)/../.."
PIDDIR="/var/run/homulili"

PIDFILE="$PIDDIR/frontend.pid"
SRCDIR="$DOCROOT/src/frontend/flask"
SRCFILE=route.py

source process_ctl.sh
