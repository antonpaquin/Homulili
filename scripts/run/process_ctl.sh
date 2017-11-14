#! /bin/bash


if [ ! -e $PIDDIR ]; then
    echo "No PID directory; Are you sure this was installed correctly?"
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
        PID=$!
        echo $PID > $PIDFILE
        renice 10 -p $PID
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
        PID=$!
        echo $PID > $PIDFILE
        renice 10 -p $PID
        popd
    else
        echo "Process not running";
    fi
fi
