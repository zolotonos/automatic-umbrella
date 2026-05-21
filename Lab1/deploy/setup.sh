#!/bin/bash
set -e

apt-get update
apt-get install -y python3 python3-pip python3-venv mariadb-server nginx git curl sudo

systemctl start mariadb
systemctl enable mariadb

mariadb -e "CREATE DATABASE IF NOT EXISTS mywebapp;"
mariadb -e "CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY '12345678';"
mariadb -e "GRANT ALL PRIVILEGES ON mywebapp.* TO 'app_user'@'localhost';"
mariadb -e "FLUSH PRIVILEGES;"

create_user_with_pass() {
    local username=$1
    useradd -m -s /bin/bash "$username" || true
    echo "$username:12345678" | chpasswd
    chage -d 0 "$username"
}

create_user_with_pass student
usermod -aG sudo student

create_user_with_pass teacher
usermod -aG sudo teacher

create_user_with_pass operator

useradd -r -s /bin/false app || true

echo "28" > /home/student/gradebook
chown student:student /home/student/gradebook

mkdir -p /opt/mywebapp
cp ../app/* /opt/mywebapp/
chown -R app:app /opt/mywebapp

python3 -m venv /opt/mywebapp/venv
/opt/mywebapp/venv/bin/pip install -r /opt/mywebapp/requirements.txt
chown -R app:app /opt/mywebapp/venv

cp operator.sudoers /etc/sudoers.d/operator
chmod 440 /etc/sudoers.d/operator

cp mywebapp.socket /etc/systemd/system/
cp mywebapp.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable --now mywebapp.socket

rm -f /etc/nginx/sites-enabled/default
cp nginx.conf /etc/nginx/sites-available/mywebapp
ln -sf /etc/nginx/sites-available/mywebapp /etc/nginx/sites-enabled/mywebapp

systemctl enable nginx
systemctl restart nginx

for u in $(awk -F: '$3 >= 1000 {print $1}' /etc/passwd); do
    if [[ "$u" != "student" && "$u" != "teacher" && "$u" != "operator" && "$u" != "nobody" ]]; then
        usermod -L "$u"
    fi
done