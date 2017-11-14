#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/scanner.pid"
SRCDIR=$DOCROOT/src/bots/scanner
SRCFILE=main.py


if [ ! -e $PIDDIR ]; then
    exit 1
fi

if [ -e $PIDFILE ]; then
    PID=$(cat $PIDFILE)
else
    PID="none"
fi

if [ "$1" == "start" ]; then
    if [ ! -e /proc/$PID -a /proc/$PID/exe ]; then
        pushd $SRCDIR
        python3 $SRCFILE &
        echo $! > $PIDFILE
        popd
    fi
fi

if [ "$1" == "stop" ]; then
    kill $PID
fi

if [ "$1" == "restart" ]; then
    kill $PID
    pushd $SRCDIR
    python3 $SRCFILE &
    echo $! > $PIDFILE
    popd
fi
