# -*- coding: utf-8 -*-
Summary: A GNU tool which simplifies the build process for users
Name: make
Version: 4.4.1
Release: 1
License: GPLv3+
URL: http://www.gnu.org/software/make/
Source: %{name}-%{version}.tar.gz

Patch0: make-4.3-getcwd.patch

# Assume we don't have clock_gettime in configure, so that
# make is not linked against -lpthread (and thus does not
# limit stack to 2MB).
Patch1: make-4.0-noclock_gettime.patch

# BZs #142691, #17374
Patch2: make-4.3-j8k.patch

# autoreconf
BuildRequires: autoconf, automake, gettext-devel
BuildRequires: perl

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

%package devel
Summary: Header file for externally visible definitions

%description devel
The make-devel package contains gnumake.h.

%prep
%autosetup -p1

rm -f tests/scripts/features/parallelism.orig

%build
autoreconf -vfi

%configure
%make_build

%install
%make_install
ln -sf make ${RPM_BUILD_ROOT}/%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}/%{_mandir}/man1/gmake.1
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang %name

%check
echo ============TESTING===============
/usr/bin/env LANG=C make check && true
echo ============END TESTING===========

%files  -f %{name}.lang
%license COPYING
%doc NEWS README AUTHORS
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_includedir}/gnumake.h

%files devel
%{_includedir}/gnumake.h
