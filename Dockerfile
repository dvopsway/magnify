############################################################
# Dockerfile to build Magnify container images
# Based on centos
############################################################

FROM  centos:6
MAINTAINER "dvopsway" padmakarojha@gmail.com
#RUN yum update

################## BEGIN INSTALLATION ######################RUN
RUN yum --assumeyes install wget
RUN /bin/bash -c " cd /root \
    && wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm \
    && rpm -ivh /root/epel-release-latest-6.noarch.rpm"
RUN yum --assumeyes --enablerepo=epel install git python-devel mysql-server mysql-devel freetds freetds-devel libjpeg libjpeg-devel openssl openssl-devel libffi libffi-devel  zlib zlib-devel -y
RUN yum --assumeyes groupinstall "Development Tools"
RUN yum --assumeyes install tar*
RUN /bin/bash -c "cd /root \
    && wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz \
    && tar -xf Python-2.7.10.tgz \
    && cd Python* \
    && ./configure --prefix=/opt/python2.7.10 --enable-shared \
    && make \
    && make install"
RUN echo "/opt/python2.7.10/lib/" > /etc/ld.so.conf.d/opt-python-2.7.10.conf
RUN ldconfig
RUN /bin/bash -c "cd /root \
    && wget https://bootstrap.pypa.io/ez_setup.py \
    && /opt/python2.7.10/bin/python ez_setup.py"
RUN /opt/python2.7.10/bin/easy_install pip
RUN /opt/python2.7.10/bin/pip install requests[security]
RUN /opt/python2.7.10/bin/pip install mysql-python django pymssql reportlab django-grappelli
RUN cd /opt/ ; git clone https://github.com/dvopsway/magnify.git
RUN yum --assumeyes install mysql mysql-server mysql-client -y
RUN service mysqld restart \
    && mysql -e "create database magnify" \
    && /opt/python2.7.10/bin/python /opt/magnify/manage.py migrate \
    && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | /opt/python2.7.10/bin/python /opt/magnify/manage.py shell
ADD magnify.sh /usr/local/bin/magnify.sh

##################### INSTALLATION END #####################
EXPOSE 80
CMD ["--port 80"]
ENTRYPOINT ["/usr/local/bin/magnify.sh"]
