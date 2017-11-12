#! /bin/bash

DOCROOT=$(pwd)/../../

if [ ! -e /var/run/homulili ]; then
    mkdir /var/run/homulili
fi

if [ -e /var/run/homulili/scraper.pid ]; then
    scraper_pid=$(cat /var/run/homulili/scraper.pid)
else
    scraper_pid="none"
fi
if [ ! -e /proc/$scraper_pid -a /proc/$scraper_pid/exe ]; then
    pushd $DOCROOT/src/bots/scraper/
    python3 main.py &
    echo $! > /var/run/homulili/scraper.pid
    popd
fi
