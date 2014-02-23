#!/bin/sh

#INSTALLATION DE L'ENV
sudo apt-get -y install python-pip
sudo apt-get install -y mysql-server
sudo apt-get -y build-dep python-mysqldb
sudo pip install MySQL-python
# Pas utile en fait il me semble
# sudo apt-get -y install libmysqlclient-dev
# sudo apt-get -y install mysql-client-core-5.5
sudo pip install Django

#INIT DE MYSQL
mysql -u root --password=$1 -e "CREATE USER 'webservices_user'@'localhost' IDENTIFIED BY 'webservices_pwd';"
mysql -u root --password=$1 -e "GRANT ALL PRIVILEGES ON *.* TO 'webservices_user'@'localhost';"
mysql -u webservices_user --password=webservices_pwd -e 'create database webservices_bdd;'

#RECUP DU PROJET
sudo apt-get -y install git
git clone https://github.com/jdugue/ghome.git

#INSTALL DES DEP REQUISES
sudo pip install requests

#INIT DU PROJET
cd ghome/webghome
python manage.py syncdb
python manage.py runserver