ARG centos=7.8.2003
ARG image=php-7.3

FROM aursu/pearbuild:${centos}-${image}

RUN yum -y --enablerepo=bintray-php73custom install \
        php-pecl-igbinary-devel \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
