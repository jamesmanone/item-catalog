#!/bin/bash
echo "Updating apt-get"
apt-get -qqy update
apt-get -qqy upgrade
echo "Instaling dependencies"
echo "This may take a while..."
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-pip
echo "Instaling python pachages"
echo "Don't despair; You're almost there!"
pip install -q --upgrade pip
pip install -q flask
pip install -q flask-sqlalchemy
pip install -q oauth2client
pip install -q requests
pip install -q httplib2
echo "Configuring database"
runuser -l postgres -c "psql -c \"CREATE USER weblink WITH PASSWORD '12345' CREATEDB;\""
runuser -l postgres -c "psql -c \"CREATE DATABASE catalog OWNER weblink\""
/vagrant/dbinit.py
echo "The server is now set up. To log into this server type \"vagrant ssh\" from this directory in terminal"
echo "Once you log in, type \"/vagrant/app.py\" to start the server"
exit
