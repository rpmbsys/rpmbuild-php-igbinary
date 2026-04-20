ARG os=8.10.20240528
ARG image=php-5.6

FROM aursu/pearbuild:${os}-${image}

RUN dnf -y --repo=bintray-phpcustom install \
        php-pecl-igbinary-devel-2.0.8 \
    && dnf clean all && rm -rf /var/cache/dnf /var/lib/rpm/__db*
