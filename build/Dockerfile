ARG centos=7
ARG image=php-7.1

FROM aursu/pearbuild:${centos}-${image}

RUN yum -y --disablerepo=* --enablerepo=custom install \
        php-pecl-igbinary-devel \
    && yum clean all && rm -rf /var/cache/yum
