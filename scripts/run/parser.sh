#! /bin/bash

DOCROOT=$(pwd)/../../

if [ ! -e /var/run/homulili ]; then
    exit 1
fi

if [ -e /var/run/homulili/parser.pid ]; then
    parser_pid=$(cat /var/run/homulili/parser.pid)
else
    parser_pid="none"
fi
if [ ! -e /proc/$parser_pid -a /proc/$parser_pid/exe ]; then
    pushd $DOCROOT/src/bots/parser
    python3 main.py &
    echo $! > /var/run/homulili/parser.pid
    popd
fi
