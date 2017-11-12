#! /bin/bash

DOCROOT=$(pwd)/../../

if [ ! -e /var/run/homulili ]; then
    exit 1
fi

if [ -e /var/run/homulili/scanner.pid ]; then
    scanner_pid=$(cat /var/run/homulili/scanner.pid)
else
    scanner_pid="none"
fi
if [ ! -e /proc/$scanner_pid -a /proc/$scanner_pid/exe ]; then
    pushd $DOCROOT/src/bots/scanner
    python3 main.py &
    echo $! > /var/run/homulili/scanner.pid
    popd
fi
