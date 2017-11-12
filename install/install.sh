#! /bin/bash

DOCROOT=$(pwd)/..

mkdir /var/run/homulili
chmod 777 /var/run/homulili

pushd $DOCROOT/install
python3 fmt_config.py &&
./postgres.sh
popd

pushd $DOCROOT/scripts
sudo -u postgres python3 run_migrations.py
popd
