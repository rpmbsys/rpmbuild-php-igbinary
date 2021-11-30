# Fedora spec file for php-pecl-igbinary
#
# Copyright (c) 2010-2021 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%define _debugsource_template %{nil}
%define debug_package %{nil}

%global pecl_name  igbinary
%global with_zts   0%{?__ztsphp:1}
%global ini_name   40-%{pecl_name}.ini

%global upstream_version 3.2.6
#global upstream_prever  RC1

Summary:        Replacement for the standard PHP serializer
Name:           php7-pecl-igbinary
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        1%{?dist}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz
License:        BSD

URL:            https://pecl.php.net/package/igbinary

BuildRequires:  gcc
BuildRequires:  php7-pear
BuildRequires:  php7-devel >= 7.3
BuildConflicts: php-devel
BuildRequires:  php7-pecl-apcu-devel

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-%{pecl_name} = %{version}
Provides:       php7-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php7-%{pecl_name}%{?_isa} = %{version}

%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation,
igbinary stores PHP data structures in a compact binary form.
Savings are significant when using memcached or similar memory
based storages for serialized data.

%package devel
Summary:       Igbinary developer files (header)
Requires:      php7-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
Requires:      php7-devel%{?_isa}

%description devel
These are the files needed to compile programs using Igbinary

%prep
%setup -q -c
mv %{pecl_name}-%{upstream_version}%{?upstream_prever} NTS

sed -e '/COPYING/s/role="doc"/role="src"/' -i package.xml

cd NTS

# Check version
subdir="php$(%{__php} -r 'echo (PHP_MAJOR_VERSION < 7 ? 5 : 7);')"
sed -e '/PHP_IGBINARY_VERSION/s/3.2.4/%{version}/' -i src/$subdir/igbinary.h

extver=$(sed -n '/#define PHP_IGBINARY_VERSION/{s/.* "//;s/".*$//;p}' src/$subdir/igbinary.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
cd ..

cat <<EOF | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Enable or disable compacting of duplicate strings
; The default is On.
;igbinary.compact_strings=On

; Use igbinary as session serializer
;session.serialize_handler=igbinary

; Use igbinary as APC serializer
;apc.serializer=igbinary
EOF

%build
cd NTS
%{_bindir}/phpize7
%configure --with-php-config=%{_bindir}/php7-config
make %{?_smp_mflags}

%install
make install -C NTS INSTALL_ROOT=%{buildroot}

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f $i       ] && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
   [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done

%check
MOD=""
# drop extension load from phpt
sed -e '/^extension=/d' -i ?TS/tests/*phpt

: simple NTS module load test, without APC, as optional
%{_bindir}/php7 --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

# APC required for test 045
if [ -f %{php_extdir}/apcu.so ]; then
  MOD="-d extension=apcu.so"
fi
if [ -f %{php_extdir}/json.so ]; then
  MOD="$MOD -d extension=json.so"
fi

: upstream test suite
cd NTS

# PHP 7.4 serrializatin error
rm -f tests/__serialize_012.phpt

TEST_PHP_EXECUTABLE=%{_bindir}/php7 \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php7 -n run-tests.php -x --show-diff

%files
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%changelog
* Thu Oct 28 2021 Remi Collet <remi@remirepo.net> - 3.2.6-1
- update to 3.2.6

* Mon Apr 19 2021 Remi Collet <remi@remirepo.net> - 3.2.2-1
- update to 3.2.2

* Mon Jan  4 2021 Remi Collet <remi@remirepo.net> - 3.2.1-1
- update to 3.2.1

* Fri Jan 17 2020 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1

* Thu Mar 21 2019 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1 (no change)

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0
- no API change
- raise dependency on PHP 7

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 Remi Collet <remi@remirepo.net> - 2.0.8-1
- update to 2.0.8

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 2.0.7-3
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Remi Collet <remi@remirepo.net> - 2.0.7-1
- update to 2.0.7

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 2.0.6-1
- update to 2.0.6 (stable)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Remi Collet <remi@remirepo.net> - 2.0.5-2
- undefine _strict_symbol_defs_build

* Mon Nov  6 2017 Remi Collet <remi@remirepo.net> - 2.0.5-1
- update to 2.0.5 (stable)

* Mon Oct 16 2017 Remi Collet <remi@remirepo.net> - 2.0.5~RC1-1
- update to 2.0.5RC1 (beta)

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 2.0.4-4
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 24 2017 Remi Collet <remi@remirepo.net> - 2.0.4-1
+- Update to 2.0.4

* Thu Apr 13 2017 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3
- tarball generated from github (not yet available on pecl)
- add patch "Don't call __wakeup if Serializable::unserialize() was used
  to build object" from https://github.com/igbinary/igbinary/pull/130
- add patch "Fix test suite for PHP 7.2"
  from https://github.com/igbinary/igbinary/pull/131

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Mon Nov 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.2.20161018git6a2d5b7
- refresh with sources from igbinary instead of old closed repo igbinary7
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.1.20151217git2b7c703
- update to 1.2.2dev for PHP 7
- ignore test results, 4 failed tests: igbinary_009.phpt, igbinary_014.phpt
  igbinary_026.phpt and igbinary_unserialize_v1_compatible.phpt
- session support not yet available

* Wed Feb 10 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- drop scriptlets (replaced by file triggers in php-pear)
- cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- open https://github.com/igbinary/igbinary/pull/36

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.12.gitc35d48f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.11.gitc35d48f
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.10.gitc35d48f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.9.gitc35d48f
- add numerical prefix to extension configuration file

* Mon Mar 10 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.8.gitc35d48f
- cleanups and drop SCL support
- install doc in pecl_docdir
- install tests in pecl_testdir (devel)

* Mon Jul 29 2013 Remi Collet <rcollet@redhat.com> - 1.1.2-0.7.gitc35d48f
- adapt for scl

* Sat Jul 27 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.6.gitc35d48f
- latest snapshot
- fix build with APCu
- spec cleanups

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.1.2-0.5.git3b8ab7e
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.4.git3b8ab7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.3.git3b8ab7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Collet <remi@fedoraproject.org> - 1.1.2-0.2.git3b8ab7e
- enable ZTS extension

* Fri Jan 20 2012 Collet <remi@fedoraproject.org> - 1.1.2-0.1.git3b8ab7e
- update to git snapshot for php 5.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 18 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-3
- fix EPEL-6 build, no arch version for php-devel

* Sat Sep 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- clean spec, adapted filters

* Mon Mar 14 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- version 1.1.1 published on pecl.php.net
- rename to php-pecl-igbinary

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- update to 1.1.1

* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-3
- updated tests from Git.

* Sat Oct 23 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-2
- filter provides to avoid igbinary.so
- add missing %%dist

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- initital RPM