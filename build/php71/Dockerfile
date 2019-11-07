ARG centos=7
ARG image=php-7.1

FROM aursu/pearbuild:${centos}-${image}

RUN yum -y --enablerepo=custom --enablerepo=bintray-php71custom install \
        php-pecl-igbinary-devel \
    && yum clean all && rm -rf /var/cache/yum /var/cache/dnf
