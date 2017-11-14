#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/scanner.pid"
SRCDIR=$DOCROOT/src/bots/scanner
SRCFILE=main.py

source process_ctl.sh
