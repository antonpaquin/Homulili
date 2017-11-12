#! /bin/bash

DOCROOT=$(pwd)/../

if [ ! -e /var/run/homulili ]; then
    mkdir /var/run/homulili
fi

if [ -e /var/run/homulili/frontend.pid ]; then
    frontend_pid=$(cat /var/run/homulili/frontend.pid)
else
    frontend_pid="none"
fi
if [ ! -e /proc/$frontend_pid -a /proc/$frontend_pid/exe ]; then
    pushd $DOCROOT/src/frontend/flask
    python3 route.py &
    echo $! > /var/run/homulili/frontend.pid
    popd
fi
