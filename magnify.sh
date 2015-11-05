#!/bin/bash
/etc/init.d/mysqld start
/opt/python2.7.10/bin/python /opt/magnify/manage.py runserver 0.0.0.0:80
