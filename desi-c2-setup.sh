#!/usr/bin/env bash

cd /var/www
git clone https://github.com/madhavbhatt/Web-Based-Command-Control.git
mv Web-Based-Command-Control desi_command_control
cd /var/www/desi_command_control
pip install --upgrade pip
# pip3 install --upgrade pip
# pip install -r requirements.txt
# pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
# python manage.py migrate --run-syncdb
mkdir static/payloads/
chown $whoami:www-data ../desi_command_control
chmod g+w ../desi_command_control
chown $whoami:www-data db.sqlite3
chmod 664 db.sqlite3
chown -R $whoami:www-data static
chmod -R g+w static
pip install pyinstaller
