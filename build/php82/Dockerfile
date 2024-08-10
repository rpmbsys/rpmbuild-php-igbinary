ARG os=9.4.20240523
ARG image=php-8.2

FROM aursu/pearbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-igbinary-devel \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
