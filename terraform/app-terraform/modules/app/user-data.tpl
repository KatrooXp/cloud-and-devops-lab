#!/bin/bash
yum update -y

#install httpd
yum install httpd -y
systemctl start httpd
systemctl enable httpd

#install php
sudo su -
yum install -y amazon-linux-extras
amazon-linux-extras enable php7.4
yum clean metadata 
yum install -y php-cli php-pdo php-fpm php-json php-mysqlnd

#install mysql
yum install -y mysql

#download from S3 bucket
aws s3 cp s3://tf-crud-app-task-s3-bucket/php-mysql-crud /var/www/html/ --recursive

#create table in db if not exist
mysql --password=${db_password} --user=admin --host=${db_cluster} < /var/www/html/database/script.sql

#restart httpd server
systemctl restart httpd