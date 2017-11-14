#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/parser.pid"
SRCDIR=$DOCROOT/src/bots/parser
SRCFILE=main.py

source process_ctl.sh
