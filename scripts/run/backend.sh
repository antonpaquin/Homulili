#! /bin/bash

DOCROOT=$(pwd)/../../
PIDDIR="/var/run/homulili"
PIDFILE="$PIDDIR/backend.pid"
SRCDIR=$DOCROOT/src/manga_host/flask
SRCFILE=route.py


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
    else
        echo "Already running"
    fi
fi

if [ "$1" == "stop" ]; then
    if [ -e /proc/$PID -a /proc/$PID/exe ]; then
        kill $PID
    else
        echo "Process not running";
    fi
fi

if [ "$1" == "restart" ]; then
    if [ -e /proc/$PID -a /proc/$PID/exe ]; then
        kill $PID
        pushd $SRCDIR
        python3 $SRCFILE &
        echo $! > $PIDFILE
        popd
    else
        echo "Process not running";
    fi
fi

