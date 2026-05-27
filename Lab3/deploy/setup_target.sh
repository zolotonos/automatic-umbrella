#!/bin/bash
set -e
apt-get update
apt-get install -y mariadb-server nginx curl sudo ca-certificates
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
systemctl start mariadb
systemctl enable mariadb
mariadb -e "CREATE DATABASE IF NOT EXISTS mywebapp;"
mariadb -e "CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY '12345678';"
mariadb -e "GRANT ALL PRIVILEGES ON mywebapp.* TO 'app_user'@'localhost';"
mariadb -e "FLUSH PRIVILEGES;"
rm -f /etc/nginx/sites-enabled/default
cp nginx.conf /etc/nginx/sites-available/mywebapp
ln -sf /etc/nginx/sites-available/mywebapp /etc/nginx/sites-enabled/mywebapp
systemctl restart nginx
systemctl enable nginx
mkdir -p /opt/mywebapp