#!/usr/bin/env bash

apt-get update
apt-get install python python3 -y
pip install --upgrade pip
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
chown $whoami:www-data ../desi_command_control
chmod g+w ../desi_command_control
chown $whoami:www-data db.sqlite3
chmod 664 db.sqlite3
chmod g+w static
chown -R $whoami:www-data static
pip3 install pyinstaller