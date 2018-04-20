# Deploy Note

apt-get update
apt-get install git python3-pip
apt-get install virtualenv
apt-get install mysql-server mysql-client
apt-get install libmysqlclient-dev
mysql -uroot
vim /etc/mysql/mysql.conf.d/mysqld.cnf
character_set_server=utf8
service mysql restart
mysql -uroot
show variables like '%char%'
create database jobplus;
exit

mkdir /srv/www
cd /srv/www
git clone https://github.com/louplus/jobplusX-Y
配置文件 ~/.pip/pip.conf

[global]
index-url=https://pypi.douban.com/simple/

[install]
trusted-host=pypi.douban.com
export LC_ALL="en_US.UTF-8"
virtualenv -p python3 venv
source ./venv/bin/activate
pip3 install -r requirements.txt
cat requirements.txt
pip3 freeze

export FLASK_APP=manage.py
flask shell
from jobplus.app import db
db.create_all()

flask run

pip3 install gunicorn
gunicorn -h

命令方式 - 开发阶段使用

gunicorn -b '0.0.0.0:8080' -w 3 manage:app
绑定到 8080 端口 指定 worker 数量
CPU 核2倍+1

gunicorn -c ./etc/gunicorn.py manage:app

配置文件的方式

gunicorn manage:app -c /srv/www/jobplus/etc/gunicorn.py

-----------------

apt-get install supervisor
cd /etc/supervisor/conf.d
jobplus.conf

update june

supervisord -c /etc/supervisor/supervisord.conf
ps -ef | grep supervisord
ps -ef | grep gunicorn


cd /etc/supervisor
supervisorctl stop all
ps aux | grep gunicorn

------------


apt-get install nginx

vim /etc/nginx/nginx.conf

cd /etc/nginx/sites-available

default

proxy_pass http://127.0.0.1:8000;


location /static {
    root /srv/www/jobplus/jobplus;
    expires 3h;
    access_log off;
}


service nginx restart
service nginx reload

nginx/error.log access.log


