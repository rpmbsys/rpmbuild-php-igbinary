ARG os=10.3.20261112.0
ARG image=php-8.1

FROM aursu/pearbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-igbinary-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
