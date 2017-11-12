#! /bin/bash

DOCROOT=$(pwd)/../../

if [ ! -e /var/run/homulili ]; then
    mkdir /var/run/homulili
fi

if [ -e /var/run/homulili/backend.pid ]; then
    backend_pid=$(cat /var/run/homulili/backend.pid)
else
    backend_pid="none"
fi
if [ ! -e /proc/$backend_pid -a /proc/$backend_pid/exe ]; then
    pushd $DOCROOT/src/manga_host/flask
    python3 route.py &
    echo $! > /var/run/homulili/backend.pid
    popd
fi
