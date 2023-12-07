ARG os=8.8.20230518
ARG image=php-8.3

FROM aursu/pearbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-igbinary-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
