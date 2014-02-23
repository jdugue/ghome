#!/bin/sh

echo Reset de la base de donnée !!
mysql -u webservices_user --password=$1 -e 'drop database webservices_bdd;'
mysql -u webservices_user --password=$1 -e 'create database webservices_bdd;'
echo OK !
echo syncdb
python manage.py syncdb

# VAR=$(expect -c '

# 	spawn python manage.py syncdb

# 	expect {
# 		"You just installed Django's auth system, which means you don't have any superusers defined.
# 		Would you like to create one now? (yes/no): "{ send "yes\r"; exp_continue }
# 	}
# 	expect {
# 		"Email address: "{ send "admin@hexanhome.com\r"; exp_continue }
# 	}
# 	expect {
# 		"Password: "{ send "admin\r"; exp_continue }
# 	}
# 	expect {
# 		"Password (again): "{ send "admin\r"; exp_continue }
# 	}

# 	puts "Finished OK"
# ')

# echo "$VAR"

# expect "Would you like to create one now? (yes/no): "
# 	send "yes"
# 	expect "Email address: "
# 	send "admin@hexanhome.com"
# 	expect "Password: "
# 	send "admin"
# 	expect "Password (again): "
# 	send "admin"