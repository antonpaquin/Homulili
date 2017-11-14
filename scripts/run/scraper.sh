#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/scraper.pid"
SRCDIR=$DOCROOT/src/bots/scraper
SRCFILE=main.py

source process_ctl.sh
