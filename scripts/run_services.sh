#! /bin/bash

DOCROOT=$(pwd)/../


if [ ! -e /var/run/homulili ]; then
    mkdir /var/run/homulili
fi


if [ -e /var/run/homulili/parser.pid ]; then
    parser_pid=$(cat /var/run/parser.pid)
else
    parser_pid="none"
fi
if [ ! -e /proc/$parser_pid -a /proc/$parser_pid/exe ]; then
    python3 $DOCROOT/src/bots/parser/main.py &
    echo $! > /var/run/homulili/parser.pid
fi


if [ -e /var/run/homulili/scanner.pid ]; then
    scanner_pid=$(cat /var/run/homulili/scanner.pid)
else
    scanner_pid="none"
fi
if [ ! -e /proc/$scanner_pid -a /proc/$scanner_pid/exe ]; then
    python3 $DOCROOT/src/bots/scanner/main.py &
    echo $! > /var/run/homulili/scanner.pid
fi


if [ -e /var/run/homulili/scraper.pid ]; then
    scraper_pid=$(cat /var/run/homulili/scraper.pid)
else
    scraper_pid="none"
fi
if [ ! -e /proc/$scraper_pid -a /proc/$scraper_pid/exe ]; then
    python3 $DOCROOT/src/bots/scraper/main.py &
    echo $! > /var/run/homulili/scraper.pid
fi


if [ -e /var/run/homulili/frontend.pid ]; then
    frontend_pid=$(cat /var/run/homulili/frontend.pid)
else
    frontend_pid="none"
fi
if [ ! -e /proc/$frontend_pid -a /proc/$frontend_pid/exe ]; then
    python3 $DOCROOT/src/frontend/flask/route.py &
    echo $! > /var/run/homulili/frontend.pid
fi


if [ -e /var/run/homulili/backend.pid ]; then
    backend_pid=$(cat /var/run/homulili/backend.pid)
else
    backend_pid="none"
fi
if [ ! -e /proc/$backend_pid -a /proc/$backend_pid/exe ]; then
    python3 $DOCROOT/src/manga_host/flask/route.py &
    echo $! > /var/run/homulili/backend.pid
fi
