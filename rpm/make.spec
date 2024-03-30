# -*- coding: utf-8 -*-
Summary: A GNU tool which simplifies the build process for users
Name: make
Version: 4.4.1
Release: 1
License: GPLv3+
URL: https://www.gnu.org/software/make/
Source: make-%{version}.tar.bz2
Source1: polist.inc
%include rpm/polist.inc

# Assume we don't have clock_gettime in configure, so that
# make is not linked against -lpthread (and thus does not
# limit stack to 2MB).
# Patch2: make-4.0-noclock_gettime.patch

# BZs #142691, #17374
# Patch3: make-4.2-j8k.patch

# autoreconf
BuildRequires: autoconf, automake, gettext-devel, texinfo
BuildRequires: perl
BuildRequires: gcc

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

# bootstrap po files ourself
for source in %{sources} ; do
    case $source in
        *.po) cp $source po/. ;;
        *) : ;;
    esac
done
(cd po;find -name \*.po) | sed -r 's/\.\/(.*).po/\1/' > po/LINGUAS

# Set tarball-version so the gnu version script picks it up
# to set the application version
echo %{version} | cut -d '+' -f 1 > .tarball-version
cp .tarball-version .version

./bootstrap --skip-po --no-git --no-bootstrap-sync --gnulib-srcdir=../gnulib

echo $PATH
cat /.build.command

cat /.build/build


%build
%configure

%make_build


%install
%make_install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/gmake.1
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang %name

# gnumake.h was introduced in 4.0, looks useless
rm %{buildroot}%{_includedir}/gnumake.h

%check
%make_build check || {
  for f in tests/work/*/*.diff*; do
    test -f "$f" || continue
    printf "++++++++++++++ %s ++++++++++++++\n" "${f##*/}"
    cat "$f"
  done
}

%files  -f %{name}.lang
%license COPYING
%doc NEWS README AUTHORS
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*
