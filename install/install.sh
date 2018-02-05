#! /bin/bash

DOCROOT=$(pwd)/..

mkdir /var/run/homulili
chmod 777 /var/run/homulili

mkdir /var/log/homulili
chmod 777 /var/log/homulili

pushd $DOCROOT/install
python3 fmt_config.py &&
chmod 777 postgres.sh &&
./postgres.sh
popd

pushd $DOCROOT/scripts
sudo -u postgres ./migrations.py run backend up
popd
