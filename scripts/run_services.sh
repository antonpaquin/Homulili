#! /bin/bash

DOCROOT=$(pwd)/../

parser_pid = $(cat /var/run/parser.pid)
if [ ! -e /proc/$parser_pid -a /proc/$parser_pid/exe ]; then
    python3 $DOCROOT/src/bots/parser/main.py &
    echo $! > /var/run/parser.pid
fi

scanner_pid = $(cat /var/run/scanner.pid)
if [ ! -e /proc/$scanner_pid -a /proc/$scanner_pid/exe ]; then
    python3 $DOCROOT/src/bots/scanner/main.py &
    echo $! > /var/run/scanner.pid
fi

scraper_pid = $(cat /var/run/scraper.pid)
if [ ! -e /proc/$scraper_pid -a /proc/$scraper_pid/exe ]; then
    python3 $DOCROOT/src/bots/scraper/main.py &
    echo $! > /var/run/scraper.pid
fi

frontend_pid = $(cat /var/run/frontend.pid)
if [ ! -e /proc/$frontend_pid -a /proc/$frontend_pid/exe ]; then
    python3 $DOCROOT/src/bots/frontend/main.py &
    echo $! > /var/run/frontend.pid
fi

backend_pid = $(cat /var/run/backend.pid)
if [ ! -e /proc/$backend_pid -a /proc/$backend_pid/exe ]; then
    python3 $DOCROOT/src/bots/backend/main.py &
    echo $! > /var/run/backend.pid
fi
