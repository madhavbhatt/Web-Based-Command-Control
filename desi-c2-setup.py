#!/usr/bin/env python

import socket, os
import subprocess
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

SECRET_KEY = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
ca = "/etc/apache2/ssl/server.crt"
key = "/etc/apache2/ssl/server.key"
var = {'ip': ip, 'ca': ca, 'key': key}

install_apache_python = ["apt-get update", "apt-get install apache2 -y", "apt-get install python python3 -y",
                         "apt-get install python-pip python3-pip -y"]

for command in install_apache_python:
    os.system(command)

desi_command_control = """
<VirtualHost *:80>
	Redirect "/" "https://{ip}/"
	ErrorLog ${{APACHE_LOG_DIR}}/error.log
	CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</VirtualHost>
"""

desi_command_control_ssl = """ 
<IfModule mod_ssl.c>
	<VirtualHost _default_:443>

		ServerAdmin webmaster@localhost
		DocumentRoot /var/www/desi_command_control
		ErrorLog ${{APACHE_LOG_DIR}}/error.log
		CustomLog ${{APACHE_LOG_DIR}}/access.log combined
		SSLEngine on

		Alias /static /var/www/desi_command_control/static
        	<Directory /var/www/desi_command_control>
                	<Files wsgi.py>
                        	Require all granted
                	</Files>
        	</Directory>
       	 	<Directory /var/www/desi_command_control/static>
        	        Require all granted
	        </Directory>
        	WSGIDaemonProcess desi_command_control python-path=/var/www/desi_command_control
        	WSGIProcessGroup desi_command_control
	        WSGIScriptAlias / /var/www/desi_command_control/desi_command_control/wsgi.py
		SSLCertificateFile	/etc/apache2/ssl/server.crt
		SSLCertificateKeyFile /etc/apache2/ssl/server.key

		<FilesMatch "\.(cgi|shtml|phtml|php)$">
				SSLOptions +StdEnvVars
		</FilesMatch>

		<Directory /usr/lib/cgi-bin>
				SSLOptions +StdEnvVars
		</Directory>
	</VirtualHost>
</IfModule>

"""

file1 = open("/etc/apache2/sites-available/desi_command_control.conf", 'w+')
file1.write(desi_command_control.format(**var))
file1.close()

file2 = open("/etc/apache2/sites-available/desi-command-control-ssl.conf", 'w+')
file2.write(desi_command_control_ssl.format(**var))
file2.close()

file3 = open("/etc/secret_key_desi_c2.txt", 'w+')
file3.write(SECRET_KEY)
file3.close()

os.chdir("/var/www")
os.system("git clone https://github.com/madhavbhatt/Web-Based-Command-Control.git")
os.system("mv Web-Based-Command-Control desi_command_control")
os.chdir("/var/www/desi_command_control/")

# "python3 manage.py collectstatic"

c2_setup_commands = ["apt-get install python-django -y", "apt-get install libapache2-mod-wsgi -y", "apt-get install python-setuptools -y",
                     "pip install django-sslserver", "pip install django-mfa","python manage.py makemigrations", "python manage.py migrate",
                     "mkdir static/payloads/", "python manage.py collectstatic",
                     "chown $whoami:www-data ../desi_command_control", "chmod g+w ../desi_command_control",
                     "chown $whoami:www-data db.sqlite3", "chmod 664 db.sqlite3", "chown -R $whoami:www-data static",
                     "chmod -R g+w static", "pip install pyinstaller"]

apache_commands = ["mkdir /etc/apache2/ssl", "a2enmod wsgi", "a2enmod ssl" ,
                   "openssl req -subj '/CN=Temporary Cert/O=Temporary Cert/C=US' -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -keyout /etc/apache2/ssl/server.key -out /etc/apache2/ssl/server.crt",
                   "a2dissite 000-default.conf", "a2ensite desi_command_control.conf",
                   "a2ensite desi-command-control-ssl.conf",
                   ]

securing_apache = ["sed 's|Options Indexes FollowSymLinks|Options FollowSymLinks|g' /etc/apache2/apache2.conf -i",
                   "sed 's|ServerSignature On|ServerSignature Off|g' /etc/apache2/conf-available/security.conf -i",
                   "sed 's|ServerTokens OS|ServerTokens Prod|g' /etc/apache2/conf-available/security.conf -i",
                   "service apache2 restart"]

for command in c2_setup_commands:
    os.system(command)

for ensite in apache_commands:
    os.system(ensite)

for line in securing_apache:
    os.system(line)

os.system("python manage.py createsuperuser")
print("Go to https://" + str(ip))

"""
apt-get install python-django -y
apt-get install libapache2-mod-wsgi -y
apt-get install python-setuptools -y
a2enmod wsgi
pip install django-sslserver
# pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
mkdir static/payloads/
chown $whoami:www-data ../desi_command_control
chmod g+w ../desi_command_control
chown $whoami:www-data db.sqlite3
chmod 664 db.sqlite3
chown -R $whoami:www-data static
chmod -R g+w static
pip install pyinstaller
"""