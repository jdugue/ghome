#!/bin/sh
echo "Entrez à nouveau votre adresse mail :"
read mail
echo $mail
echo "Entrez à nouveau votre mot de passe d'admin :"
read -s pass
echo $pass
server/configweb.cfg > [web_info] \ruser = $mail\rpasswd = $pass