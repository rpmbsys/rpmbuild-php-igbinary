ARG os=8.10.20240528
ARG image=php-apcu-5.6

FROM aursu/peclbuild:${os}-${image}

COPY SOURCES ${BUILD_TOPDIR}/SOURCES
COPY SPECS ${BUILD_TOPDIR}/SPECS

RUN chown -R $BUILD_USER ${BUILD_TOPDIR}/{SOURCES,SPECS}

USER $BUILD_USER

ENTRYPOINT ["/usr/bin/rpmbuild", "php-pecl-igbinary.spec"]
CMD ["-ba"]
