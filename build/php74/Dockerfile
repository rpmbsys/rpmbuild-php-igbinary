ARG centos=7
ARG image=php-7.4

FROM aursu/pearbuild:${centos}-${image}

RUN yum -y --enablerepo=custom --enablerepo=bintray-php74custom install \
        php-pecl-igbinary-devel \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
