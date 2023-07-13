# See http://bugzilla.redhat.com/223663
%global multilib_archs x86_64 %{ix86} %{?mips} ppc64 ppc s390x s390 sparc64 sparcv9
%global multilib_basearchs x86_64 %{?mips64} ppc64 s390x sparc64

%global openssl -openssl-linked

# support qtchooser (adds qtchooser .conf file)
%global qtchooser 1
%if 0%{?qtchooser}
%global priority 10
%ifarch %{multilib_basearchs}
%global priority 15
%endif
%endif

%global platform linux-g++

%if 0%{?use_clang}
%global platform linux-clang
%endif

%if "%toolchain" == "clang"
%global platform linux-clang
%endif

%global qt_module qtbase

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%global journald -journald
BuildRequires:    make
BuildRequires:    pkgconfig(libsystemd)

%global examples 1
## skip for now, until we're better at it --rex
#global tests 1

Name:             qt5-qtbase
Summary:          Qt5 - QtBase components
Version:          5.15.2
Release:          7


# See LGPL_EXCEPTIONS.txt, for exception details
License:          LGPLv2 with exceptions or GPLv3 with exceptions
Url:              http://qt-project.org/
%global  majmin %(echo %{version} | cut -d. -f1-2)
Source0:          https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1227295
Source1:          qtlogging.ini

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1036956
Source2:          qconfig-multilib.h

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source3:          10-qt5-check-opengl2.sh

# macros
Source4:          macros.qt5-qtbase

# borrowed from opensuse
# track private api via properly versioned symbols
# downside: binaries produced with these differently-versioned symbols are no longer
# compatible with qt-project.org's Qt binary releases.
Patch0001:        tell-the-truth-about-private-api.patch

# upstreamable patches
# namespace QT_VERSION_CHECK to workaround major/minor being pre-defined (#1396755)
Patch0002:        qtbase-opensource-src-5.8.0-QT_VERSION_CHECK.patch

# 1. Workaround moc/multilib issues
# https://bugzilla.redhat.com/show_bug.cgi?id=1290020
# https://bugreports.qt.io/browse/QTBUG-49972
# 2. Workaround sysmacros.h (pre)defining major/minor a breaking stuff
Patch0004:        qtbase-opensource-src-5.7.1-moc_macros.patch

# CMake generates wrong -isystem /usr/include compilations flags with Qt5::Gui
# https://bugzilla.redhat.com/1704474
Patch0005:        qtbase-everywhere-src-5.12.1-qt5gui_cmake_isystem_includes.patch

# respect QMAKE_LFLAGS_RELEASE when building qmake
Patch0006:        qtbase-qmake_LFLAGS.patch

# don't use relocatable heuristics to guess prefix when using -no-feature-relocatable
Patch0007:        qtbase-everywhere-src-5.14.2-no_relocatable.patch

# drop -O3 and make -O2 by default
Patch0008:        qt5-qtbase-cxxflag.patch

# support firebird version 3.x
Patch0009:        qt5-qtbase-5.12.1-firebird.patch

# fix for new mariadb
Patch0010:        qtbase-opensource-src-5.9.0-mysql.patch

# python3
Patch0011:        qtbase-everywhere-src-5.11.1-python3.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1732129
Patch0012:        qtbase-use-wayland-on-gnome.patch

# gcc-11
Patch0013:        %{name}-gcc11.patch

# glibc stat

## upstream patches
# see also patch90
Patch0014:        qtbase-QTBUG-90395.patch
Patch0015:        qtbase-QTBUG-89977.patch
Patch0017:        qtbase-QTBUG-91909.patch
Patch0018:        0001-modify-kwin_5.18-complier-error.patch
# https://launchpad.net/ubuntu/+source/qtbase-opensource-src/5.15.2+dfsg-15
Patch0019:        CVE-2021-38593.patch
Patch0020:        CVE-2022-25255.patch
Patch0021:        qt5-qtbase-Add-sw64-architecture.patch
Patch0022:        add-loongarch64-support.patch
# https://download.qt.io/official_releases/qt/5.15/CVE-2023-24607-qtbase-5.15.diff
Patch0023:        CVE-2023-24607.patch
# Do not check any files in %%{_qt5_plugindir}/platformthemes/ for requires.
# Those themes are there for platform integration. If the required libraries are
# not there, the platform to integrate with isn't either. Then Qt will just
# silently ignore the plugin that fails to load. Thus, there is no need to let
# RPM drag in gtk3 as a dependency for the GTK+3 dialog support.
%global __requires_exclude_from ^%{_qt5_plugindir}/platformthemes/.*$
# filter plugin provides
%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$

BuildRequires:    cups-devel
BuildRequires:    desktop-file-utils
BuildRequires:    findutils
BuildRequires:    libjpeg-devel
BuildRequires:    libmng-devel
BuildRequires:    libtiff-devel
BuildRequires:    pkgconfig(alsa)
# required for -accessibility
BuildRequires:    pkgconfig(atspi-2)
%if 0%{?use_clang}
BuildRequires:    clang >= 3.7.0
%else
BuildRequires:    gcc-c++
%endif
# http://bugzilla.redhat.com/1196359

%global dbus -dbus-linked
BuildRequires:    pkgconfig(dbus-1)

BuildRequires:    pkgconfig(libdrm)
BuildRequires:    pkgconfig(fontconfig)
BuildRequires:    pkgconfig(gl)
BuildRequires:    pkgconfig(glib-2.0)
BuildRequires:    pkgconfig(gtk+-3.0)
BuildRequires:    pkgconfig(libproxy-1.0)
# xcb-sm
BuildRequires:    pkgconfig(ice) pkgconfig(sm)
BuildRequires:    pkgconfig(libpng)
BuildRequires:    pkgconfig(libudev)
BuildRequires:    openssl-devel
BuildRequires:    pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires:    pkgconfig(libinput)
BuildRequires:    pkgconfig(xcb-xkb) >= 1.10
BuildRequires:    pkgconfig(xcb-util)
BuildRequires:    pkgconfig(xkbcommon) >= 0.4.1
BuildRequires:    pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires:    pkgconfig(xkeyboard-config)
%global vulkan 1
BuildRequires:    pkgconfig(vulkan)

%global egl 1
BuildRequires:    libEGL-devel
BuildRequires:    pkgconfig(gbm)
## TODO: apparently only needed if building opengl_es2 support, do we actually use it?  -- rex
BuildRequires:    pkgconfig(glesv2)
%global sqlite -system-sqlite
BuildRequires:    pkgconfig(sqlite3) >= 3.7

%global harfbuzz -system-harfbuzz
BuildRequires:    pkgconfig(harfbuzz) >= 0.9.42

BuildRequires:    pkgconfig(icu-i18n)
BuildRequires:    pkgconfig(libpcre2-posix) >= 10.20
BuildRequires:    pkgconfig(libpcre) >= 8.0
%global pcre -system-pcre
BuildRequires:    pkgconfig(xcb-xkb)

BuildRequires:    libicu-devel
%global pcre -qt-pcre

BuildRequires:    pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)
BuildRequires:    pkgconfig(zlib)
BuildRequires:    perl-generators
# see patch68
BuildRequires:    python3
BuildRequires:    qt5-rpm-macros

%if 0%{?tests}
BuildRequires:    dbus-x11
BuildRequires:    mesa-dri-drivers
BuildRequires:    time
BuildRequires:    xorg-x11-server-Xvfb
%endif

%if 0%{?qtchooser}

Conflicts:        qt < 1:4.8.6-10

Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%endif
Requires:         qt-settings
Requires:         %{name}-common = %{version}-%{release}

## Sql drivers

%global ibase -no-sql-ibase
%global tds -no-sql-tds


# workaround gold linker bug(s) by not using it
# https://bugzilla.redhat.com/1458003
# https://sourceware.org/bugzilla/show_bug.cgi?id=21074
# reportedly fixed or worked-around, re-enable if there's evidence of problems -- rex
# https://bugzilla.redhat.com/show_bug.cgi?id=1635973
%global use_gold_linker -no-use-gold-linker

%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary:          Common files for Qt5
# offer upgrade path for qtquick1 somewhere... may as well be here -- rex
Obsoletes:        qt5-qtquick1 < 5.9.0
Obsoletes:        qt5-qtquick1-devel < 5.9.0
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch
%description common
%{summary}.

%package devel
Summary:          Development files for %{name}
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-gui%{?_isa}
%if 0%{?egl}
Requires:         libEGL-devel
%endif
Requires:         pkgconfig(gl)
%if 0%{?vulkan}
Requires:         pkgconfig(vulkan)
%endif
Requires:         qt5-rpm-macros
%if 0%{?use_clang}
Requires:         clang >= 3.7.0
%endif
%description devel
%{summary}.

%package private-devel
Summary:          Development files for %{name} private APIs
# upgrade path, when private-devel was introduced
Obsoletes:        %{name}-devel < 5.12.1-3
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
# QtPrintSupport/private requires cups/ppd.h
Requires:         cups-devel
%description private-devel
%{summary}.

%package examples
Summary:          Programming examples for %{name}
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description examples
%{summary}.

%package static
Summary:          Static library files for %{name}
Requires:         %{name}-devel%{?_isa} = %{version}-%{release}
Requires:         pkgconfig(fontconfig)
Requires:         pkgconfig(glib-2.0)
Requires:         pkgconfig(libinput)
Requires:         pkgconfig(xkbcommon)
Requires:         pkgconfig(zlib)

%description static
%{summary}.

%if "%{?ibase}" != "-no-sql-ibase"
%package ibase
Summary:          IBase driver for Qt5's SQL classes
BuildRequires:    firebird-devel
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%package mysql
Summary:          MySQL driver for Qt5's SQL classes

BuildRequires:    mariadb-connector-c-devel

#BuildRequires:    mysql-devel

Requires:         %{name}%{?_isa} = %{version}-%{release}
%description mysql
%{summary}.

%package odbc
Summary:          ODBC driver for Qt5's SQL classes
BuildRequires:    unixODBC-devel
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description odbc
%{summary}.

%package postgresql
Summary:          PostgreSQL driver for Qt5's SQL classes
BuildRequires:    libpq-devel
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description postgresql
%{summary}.

%if "%{?tds}" != "-no-sql-tds"
%package tds
Summary:          TDS driver for Qt5's SQL classes
BuildRequires:    freetds-devel
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description tds
%{summary}.
%endif

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary:          Qt5 GUI-related libraries
Requires:         %{name}%{?_isa} = %{version}-%{release}
Recommends:       mesa-dri-drivers
Obsoletes:        qt5-qtbase-x11 < 5.2.0
Provides:         qt5-qtbase-x11 = %{version}-%{release}
# for Source3: 10-qt5-check-opengl2.sh:
# glxinfo
Requires:         glx-utils
%description gui
Qt5 libraries used for drawing widgets and OpenGL items.


%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}

## upstream fixes

# omit '-b .tell-the-truth-about-private-api' so it doesn't end up in installed files -- rdieter
%patch0001 -p1

%patch0002 -p1 -b .QT_VERSION_CHECK
# FIXME/TODO : rebase or drop -- rdieter
#patch51 -p1 -b .hidpi_scale_at_192
%patch0004 -p1 -b .moc_macros
%patch0005 -p1 -b .qt5gui_cmake_isystem_includes
%patch0006 -p1 -b .qmake_LFLAGS
%patch0007 -p1 -b .no_relocatable
%patch0008 -p1 -b .qt5-qtbase-cxxflag
%patch0009 -p1 -b .firebird
%patch0010 -p1 -b .mysql
%patch0011 -p1
%patch0012 -p1 -b .use-wayland-on-gnome.patch
%patch0013 -p1 -b .gcc11

## upstream patches
%patch0014 -p1 -b .QTBUG-90395
%patch0015 -p1 -b .QTBUG-89977
%patch0017 -p1 -b .QTBUG-91909
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
mv freetype libjpeg libpng zlib UNUSED/
%if "%{?sqlite}" == "-system-sqlite"
mv sqlite UNUSED/
%endif
%if "%{?xcb}" != "-qt-xcb"
mv xcb UNUSED/
%endif
popd

# builds failing mysteriously on f20
# ./configure: Permission denied
# check to ensure that can't happen -- rex
test -x configure || chmod +x configure

# use proper perl interpretter so autodeps work as expected
sed -i -e "s|^#!/usr/bin/env perl$|#!%{__perl}|" \
 bin/fixqt4headers.pl \
 bin/syncqt.pl \
 mkspecs/features/data/unix/findclasslist.pl


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
# https://bugzilla.redhat.com/1900527
%define _lto_cflags %{nil}

## FIXME/TODO:
# * for %%ix86, add sse2 enabled builds for Qt5Gui, Qt5Core, QtNetwork, see also:
#   http://anonscm.debian.org/cgit/pkg-kde/qt/qtbase.git/tree/debian/rules (234-249)

## adjust $RPM_OPT_FLAGS
# remove -fexceptions
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`
RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?qt5_arm_flag} %{?qt5_deprecated_flag} %{?qt5_null_flag}"

%if 0%{?use_clang}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fno-delete-null-pointer-checks||g'`
%endif

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
export MAKEFLAGS="%{?_smp_mflags}"

./configure \
  -verbose \
  -confirm-license \
  -opensource \
  -prefix %{_qt5_prefix} \
  -archdatadir %{_qt5_archdatadir} \
  -bindir %{_qt5_bindir} \
  -libdir %{_qt5_libdir} \
  -libexecdir %{_qt5_libexecdir} \
  -datadir %{_qt5_datadir} \
  -docdir %{_qt5_docdir} \
  -examplesdir %{_qt5_examplesdir} \
  -headerdir %{_qt5_headerdir} \
  -importdir %{_qt5_importdir} \
  -plugindir %{_qt5_plugindir} \
  -sysconfdir %{_qt5_sysconfdir} \
  -translationdir %{_qt5_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -accessibility \
  %{?dbus}%{!?dbus:-dbus-runtime} \
  %{?egl:-egl} \
  -fontconfig \
  -glib \
  -gtk \
  %{?ibase} \
  -icu \
  %{?journald} \
  -optimized-qmake \
  %{?openssl} \
  %{!?examples:-nomake examples} \
  %{!?tests:-nomake tests} \
  -no-pch \
  -no-reduce-relocations \
  -no-rpath \
  -no-separate-debug-info \
  -no-strip \
  -system-libjpeg \
  -system-libpng \
  %{?harfbuzz} \
  %{?pcre} \
  %{?sqlite} \
  %{?tds} \
  %{?xcb} \
  %{?xkbcommon} \
  -system-zlib \
  %{?use_gold_linker} \
  -no-directfb \
  -no-feature-relocatable \
  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}"

# ensure qmake build using optflags (which can happen if not munging qmake.conf defaults)
make clean -C qmake
%make_build -C qmake all binary \
  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}" \
  QMAKE_STRIP=

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

install -m644 -p -D %{SOURCE1} %{buildroot}%{_qt5_datadir}/qtlogging.ini

# Qt5.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt5.pc<<EOF
prefix=%{_qt5_prefix}
archdatadir=%{_qt5_archdatadir}
bindir=%{_qt5_bindir}
datadir=%{_qt5_datadir}

docdir=%{_qt5_docdir}
examplesdir=%{_qt5_examplesdir}
headerdir=%{_qt5_headerdir}
importdir=%{_qt5_importdir}
libdir=%{_qt5_libdir}
libexecdir=%{_qt5_libexecdir}
moc=%{_qt5_bindir}/moc
plugindir=%{_qt5_plugindir}
qmake=%{_qt5_bindir}/qmake
settingsdir=%{_qt5_settingsdir}
sysconfdir=%{_qt5_sysconfdir}
translationdir=%{_qt5_translationdir}

Name: Qt5
Description: Qt5 Configuration
Version: 5.15.2
EOF

# rpm macros
install -p -m644 -D %{SOURCE4} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase

# create/own dirs
mkdir -p %{buildroot}{%{_qt5_archdatadir}/mkspecs/modules,%{_qt5_importdir},%{_qt5_libexecdir},%{_qt5_plugindir}/{designer,iconengines,script,styles},%{_qt5_translationdir}}
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject

# hardlink files to {_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    moc|qdbuscpp2xml|qdbusxml2cpp|qmake|rcc|syncqt|uic)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h %{buildroot}%{_qt5_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE2} %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h
%endif

# qtchooser conf
%if 0%{?qtchooser}
  mkdir -p %{buildroot}%{_sysconfdir}/xdg/qtchooser
  pushd    %{buildroot}%{_sysconfdir}/xdg/qtchooser
  echo "%{_qt5_bindir}" >  5-%{__isa_bits}.conf
## FIXME/TODO: verify qtchooser (still) happy if _qt5_prefix uses %%_prefix instead of %%_libdir/qt5
  echo "%{_qt5_prefix}" >> 5-%{__isa_bits}.conf
  # alternatives targets
  touch default.conf 5.conf
  popd
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -p -m755 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh

# install privat headers for qtxcb
mkdir -p %{buildroot}%{_qt5_headerdir}/QtXcb
install -m 644 src/plugins/platforms/xcb/*.h %{buildroot}%{_qt5_headerdir}/QtXcb/


%check
# verify Qt5.pc
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion Qt5)" = "%{version}"
%if 0%{?tests}
## see tests/README for expected environment (running a plasma session essentially)
## we are not quite there yet
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
# dbus tests error out when building if session bus is not available
dbus-launch --exit-with-session \
%make_build sub-tests  -k ||:
xvfb-run -a --server-args="-screen 0 1280x1024x32" \
dbus-launch --exit-with-session \
time \
make check -k ||:
%endif


%if 0%{?qtchooser}
%pre
if [ $1 -gt 1 ] ; then
# remove short-lived qt5.conf alternatives
%{_sbindir}/update-alternatives  \
  --remove qtchooser-qt5 \
  %{_sysconfdir}/xdg/qtchooser/qt5-%{__isa_bits}.conf >& /dev/null ||:

%{_sbindir}/update-alternatives  \
  --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/qt5.conf >& /dev/null ||:
fi
%endif

%post
%{?ldconfig}
%if 0%{?qtchooser}
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/qtchooser/5.conf \
  qtchooser-5 \
  %{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf \
  %{priority}

%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/xdg/qtchooser/default.conf \
  qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/5.conf \
  %{priority}
%endif

%postun
%{?ldconfig}
%if 0%{?qtchooser}
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives  \
  --remove qtchooser-5 \
  %{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf

%{_sbindir}/update-alternatives  \
  --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/5.conf
fi
%endif

%files
%license LICENSE.FDL
%license LICENSE.GPL*
%license LICENSE.LGPL*
%if 0%{?qtchooser}
%dir %{_sysconfdir}/xdg/qtchooser
# not editable config files, so not using %%config here
%ghost %{_sysconfdir}/xdg/qtchooser/default.conf
%ghost %{_sysconfdir}/xdg/qtchooser/5.conf
%{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf
%endif
%dir %{_sysconfdir}/xdg/QtProject/
%{_qt5_libdir}/libQt5Concurrent.so.5*
%{_qt5_libdir}/libQt5Core.so.5*
%{_qt5_libdir}/libQt5DBus.so.5*
%{_qt5_libdir}/libQt5Network.so.5*
%{_qt5_libdir}/libQt5Sql.so.5*
%{_qt5_libdir}/libQt5Test.so.5*
%{_qt5_libdir}/libQt5Xml.so.5*
%dir %{_qt5_libdir}/cmake/
%dir %{_qt5_libdir}/cmake/Qt5/
%dir %{_qt5_libdir}/cmake/Qt5Concurrent/
%dir %{_qt5_libdir}/cmake/Qt5Core/
%dir %{_qt5_libdir}/cmake/Qt5DBus/
%dir %{_qt5_libdir}/cmake/Qt5Gui/
%dir %{_qt5_libdir}/cmake/Qt5Network/
%dir %{_qt5_libdir}/cmake/Qt5OpenGL/
%dir %{_qt5_libdir}/cmake/Qt5PrintSupport/
%dir %{_qt5_libdir}/cmake/Qt5Sql/
%dir %{_qt5_libdir}/cmake/Qt5Test/
%dir %{_qt5_libdir}/cmake/Qt5Widgets/
%dir %{_qt5_libdir}/cmake/Qt5Xml/
%dir %{_qt5_docdir}/
%{_qt5_docdir}/global/
%{_qt5_docdir}/config/
%{_qt5_importdir}/
%{_qt5_translationdir}/
%if "%{_qt5_prefix}" != "%{_prefix}"
%dir %{_qt5_prefix}/
%endif
%dir %{_qt5_archdatadir}/
%dir %{_qt5_datadir}/
%{_qt5_datadir}/qtlogging.ini
%dir %{_qt5_libexecdir}/
%dir %{_qt5_plugindir}/
%dir %{_qt5_plugindir}/bearer/
%{_qt5_plugindir}/bearer/libqconnmanbearer.so
%{_qt5_plugindir}/bearer/libqgenericbearer.so
%{_qt5_plugindir}/bearer/libqnmbearer.so
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QConnmanEnginePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QGenericEnginePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_QNetworkManagerEnginePlugin.cmake
%dir %{_qt5_plugindir}/designer/
%dir %{_qt5_plugindir}/generic/
%dir %{_qt5_plugindir}/iconengines/
%dir %{_qt5_plugindir}/imageformats/
%dir %{_qt5_plugindir}/platforminputcontexts/
%dir %{_qt5_plugindir}/platforms/
%dir %{_qt5_plugindir}/platformthemes/
%dir %{_qt5_plugindir}/printsupport/
%dir %{_qt5_plugindir}/script/
%dir %{_qt5_plugindir}/sqldrivers/
%dir %{_qt5_plugindir}/styles/
%{_qt5_plugindir}/sqldrivers/libqsqlite.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake

%files common
# mostly empty for now, consider: filesystem/dir ownership, licenses
%{rpm_macros_dir}/macros.qt5-qtbase

%files devel
%if "%{_qt5_bindir}" != "%{_bindir}"
%dir %{_qt5_bindir}
%endif
%{_bindir}/moc*
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qmake*
%{_bindir}/rcc*
%{_bindir}/syncqt*
%{_bindir}/uic*
%{_bindir}/qlalr
%{_bindir}/fixqt4headers.pl
%{_bindir}/qvkgen
%{_bindir}/tracegen
%{_qt5_bindir}/moc*
%{_qt5_bindir}/qdbuscpp2xml*
%{_qt5_bindir}/qdbusxml2cpp*
%{_qt5_bindir}/qmake*
%{_qt5_bindir}/rcc*
%{_qt5_bindir}/syncqt*
%{_qt5_bindir}/uic*
%{_qt5_bindir}/qlalr
%{_qt5_bindir}/fixqt4headers.pl
%{_qt5_bindir}/qvkgen
%if "%{_qt5_headerdir}" != "%{_includedir}"
%dir %{_qt5_headerdir}
%endif
%{_qt5_headerdir}/QtConcurrent/
%{_qt5_headerdir}/QtCore/
%{_qt5_headerdir}/QtDBus/
%{_qt5_headerdir}/QtGui/
%{_qt5_headerdir}/QtNetwork/
%{_qt5_headerdir}/QtOpenGL/
%{_qt5_headerdir}/QtPlatformHeaders/
%{_qt5_headerdir}/QtPrintSupport/
%{_qt5_headerdir}/QtSql/
%{_qt5_headerdir}/QtTest/
%{_qt5_headerdir}/QtWidgets/
%{_qt5_headerdir}/QtXcb/
%{_qt5_headerdir}/QtXml/
%{_qt5_headerdir}/QtEglFSDeviceIntegration
%{_qt5_headerdir}/QtInputSupport
%{_qt5_headerdir}/QtEdidSupport
%{_qt5_headerdir}/QtXkbCommonSupport
%{_qt5_archdatadir}/mkspecs/
%{_qt5_libdir}/libQt5Concurrent.prl
%{_qt5_libdir}/libQt5Concurrent.so
%{_qt5_libdir}/libQt5Core.prl
%{_qt5_libdir}/libQt5Core.so
%{_qt5_libdir}/libQt5DBus.prl
%{_qt5_libdir}/libQt5DBus.so
%{_qt5_libdir}/libQt5Gui.prl
%{_qt5_libdir}/libQt5Gui.so
%{_qt5_libdir}/libQt5Network.prl
%{_qt5_libdir}/libQt5Network.so
%{_qt5_libdir}/libQt5OpenGL.prl
%{_qt5_libdir}/libQt5OpenGL.so
%{_qt5_libdir}/libQt5PrintSupport.prl
%{_qt5_libdir}/libQt5PrintSupport.so
%{_qt5_libdir}/libQt5Sql.prl
%{_qt5_libdir}/libQt5Sql.so
%{_qt5_libdir}/libQt5Test.prl
%{_qt5_libdir}/libQt5Test.so
%{_qt5_libdir}/libQt5Widgets.prl
%{_qt5_libdir}/libQt5Widgets.so
%{_qt5_libdir}/libQt5XcbQpa.prl
%{_qt5_libdir}/libQt5XcbQpa.so
%{_qt5_libdir}/libQt5Xml.prl
%{_qt5_libdir}/libQt5Xml.so
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.prl
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.so
%{_qt5_libdir}/cmake/Qt5/Qt5Config*.cmake
%{_qt5_libdir}/cmake/Qt5Concurrent/Qt5ConcurrentConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CoreMacros.cmake
%{_qt5_libdir}/cmake/Qt5Core/Qt5CTestMacros.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusConfig*.cmake
%{_qt5_libdir}/cmake/Qt5DBus/Qt5DBusMacros.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%{_qt5_libdir}/cmake/Qt5OpenGL/Qt5OpenGLConfig*.cmake
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Test/Qt5TestConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{_qt5_libdir}/cmake/Qt5Xml/Qt5XmlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5/Qt5ModuleLocation.cmake
%{_qt5_libdir}/cmake/Qt5AccessibilitySupport/
%{_qt5_libdir}/cmake/Qt5DeviceDiscoverySupport/
%{_qt5_libdir}/cmake/Qt5EdidSupport/
%{_qt5_libdir}/cmake/Qt5EglFSDeviceIntegration/
%{_qt5_libdir}/cmake/Qt5EglFsKmsSupport/
%{_qt5_libdir}/cmake/Qt5EglSupport/
%{_qt5_libdir}/cmake/Qt5EventDispatcherSupport/
%{_qt5_libdir}/cmake/Qt5FbSupport/
%{_qt5_libdir}/cmake/Qt5FontDatabaseSupport/
%{_qt5_libdir}/cmake/Qt5GlxSupport/
%{_qt5_libdir}/cmake/Qt5InputSupport/
%{_qt5_libdir}/cmake/Qt5KmsSupport/
%{_qt5_libdir}/cmake/Qt5LinuxAccessibilitySupport/
%{_qt5_libdir}/cmake/Qt5PlatformCompositorSupport/
%{_qt5_libdir}/cmake/Qt5ServiceSupport/
%{_qt5_libdir}/cmake/Qt5ThemeSupport/
%{_qt5_libdir}/cmake/Qt5XcbQpa/
%{_qt5_libdir}/cmake/Qt5XkbCommonSupport/
%{_qt5_libdir}/metatypes/qt5core_metatypes.json
%{_qt5_libdir}/metatypes/qt5gui_metatypes.json
%{_qt5_libdir}/metatypes/qt5widgets_metatypes.json
%{_qt5_libdir}/pkgconfig/Qt5.pc
%{_qt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{_qt5_libdir}/pkgconfig/Qt5Core.pc
%{_qt5_libdir}/pkgconfig/Qt5DBus.pc
%{_qt5_libdir}/pkgconfig/Qt5Gui.pc
%{_qt5_libdir}/pkgconfig/Qt5Network.pc
%{_qt5_libdir}/pkgconfig/Qt5OpenGL.pc
%{_qt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{_qt5_libdir}/pkgconfig/Qt5Sql.pc
%{_qt5_libdir}/pkgconfig/Qt5Test.pc
%{_qt5_libdir}/pkgconfig/Qt5Widgets.pc
%{_qt5_libdir}/pkgconfig/Qt5Xml.pc
%if 0%{?egl}
%{_qt5_libdir}/libQt5EglFsKmsSupport.prl
%{_qt5_libdir}/libQt5EglFsKmsSupport.so
%endif
%{_qt5_libdir}/qt5/bin/tracegen
## private-devel globs
# keep mkspecs/modules stuff  in -devel for now, https://bugzilla.redhat.com/show_bug.cgi?id=1705280
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_*_private.pri
%exclude %{_qt5_headerdir}/*/%{version}/

%files private-devel
%{_qt5_headerdir}/*/%{version}/
#{_qt5_archdatadir}/mkspecs/modules/qt_lib_*_private.pri

%files static
%{_qt5_libdir}/libQt5Bootstrap.*a
%{_qt5_libdir}/libQt5Bootstrap.prl
%{_qt5_headerdir}/QtOpenGLExtensions/
%{_qt5_libdir}/libQt5OpenGLExtensions.*a
%{_qt5_libdir}/libQt5OpenGLExtensions.prl
%{_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_qt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{_qt5_libdir}/libQt5AccessibilitySupport.*a
%{_qt5_libdir}/libQt5AccessibilitySupport.prl
%{_qt5_headerdir}/QtAccessibilitySupport
%{_qt5_libdir}/libQt5DeviceDiscoverySupport.*a
%{_qt5_libdir}/libQt5DeviceDiscoverySupport.prl
%{_qt5_headerdir}/QtDeviceDiscoverySupport
%{_qt5_libdir}/libQt5EglSupport.*a
%{_qt5_libdir}/libQt5EglSupport.prl
%{_qt5_headerdir}/QtEglSupport
%{_qt5_libdir}/libQt5EventDispatcherSupport.*a
%{_qt5_libdir}/libQt5EventDispatcherSupport.prl
%{_qt5_headerdir}/QtEventDispatcherSupport
%{_qt5_libdir}/libQt5FbSupport.*a
%{_qt5_libdir}/libQt5FbSupport.prl
%{_qt5_headerdir}/QtFbSupport
%{_qt5_libdir}/libQt5FontDatabaseSupport.*a
%{_qt5_libdir}/libQt5FontDatabaseSupport.prl
%{_qt5_headerdir}/QtFontDatabaseSupport
%{_qt5_libdir}/libQt5GlxSupport.*a
%{_qt5_libdir}/libQt5GlxSupport.prl
%{_qt5_headerdir}/QtGlxSupport
%{_qt5_libdir}/libQt5InputSupport.*a
%{_qt5_libdir}/libQt5InputSupport.prl
%{_qt5_libdir}/libQt5LinuxAccessibilitySupport.*a
%{_qt5_libdir}/libQt5LinuxAccessibilitySupport.prl
%{_qt5_headerdir}/QtLinuxAccessibilitySupport
%{_qt5_libdir}/libQt5PlatformCompositorSupport.*a
%{_qt5_libdir}/libQt5PlatformCompositorSupport.prl
%{_qt5_headerdir}/QtPlatformCompositorSupport
%{_qt5_libdir}/libQt5ServiceSupport.*a
%{_qt5_libdir}/libQt5ServiceSupport.prl
%{_qt5_headerdir}/QtServiceSupport
%{_qt5_libdir}/libQt5ThemeSupport.*a
%{_qt5_libdir}/libQt5ThemeSupport.prl
%{_qt5_headerdir}/QtThemeSupport
%{_qt5_libdir}/libQt5KmsSupport.*a
%{_qt5_libdir}/libQt5KmsSupport.prl
%{_qt5_headerdir}/QtKmsSupport
%{_qt5_libdir}/libQt5EdidSupport.*a
%{_qt5_libdir}/libQt5EdidSupport.prl
%{_qt5_libdir}/libQt5XkbCommonSupport.*a
%{_qt5_libdir}/libQt5XkbCommonSupport.prl
%if 0%{?vulkan}
%{_qt5_headerdir}/QtVulkanSupport/
%{_qt5_libdir}/cmake/Qt5VulkanSupport/
%{_qt5_libdir}/libQt5VulkanSupport.*a
%{_qt5_libdir}/libQt5VulkanSupport.prl
%endif

%if 0%{?examples}
%files examples
%{_qt5_examplesdir}/
%endif

%if "%{?ibase}" != "-no-sql-ibase"
%files ibase
%{_qt5_plugindir}/sqldrivers/libqsqlibase.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QIBaseDriverPlugin.cmake
%endif

%files mysql
%{_qt5_plugindir}/sqldrivers/libqsqlmysql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QMYSQLDriverPlugin.cmake

%files odbc
%{_qt5_plugindir}/sqldrivers/libqsqlodbc.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QODBCDriverPlugin.cmake

%files postgresql
%{_qt5_plugindir}/sqldrivers/libqsqlpsql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QPSQLDriverPlugin.cmake

%if "%{?tds}" != "-no-sql-tds"
%files tds
%{_qt5_plugindir}/sqldrivers/libqsqltds.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QTDSDriverPlugin.cmake
%endif

%ldconfig_scriptlets gui

%files gui
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d/
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%{_qt5_libdir}/libQt5Gui.so.5*
%{_qt5_libdir}/libQt5OpenGL.so.5*
%{_qt5_libdir}/libQt5PrintSupport.so.5*
%{_qt5_libdir}/libQt5Widgets.so.5*
%{_qt5_libdir}/libQt5XcbQpa.so.5*
%{_qt5_plugindir}/generic/libqevdevkeyboardplugin.so
%{_qt5_plugindir}/generic/libqevdevmouseplugin.so
%{_qt5_plugindir}/generic/libqevdevtabletplugin.so
%{_qt5_plugindir}/generic/libqevdevtouchplugin.so
%{_qt5_plugindir}/generic/libqlibinputplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLibInputPlugin.cmake
%{_qt5_plugindir}/generic/libqtuiotouchplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevKeyboardPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevMousePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTabletPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTouchScreenPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QTuioTouchPlugin.cmake
%{_qt5_plugindir}/imageformats/libqgif.so
%{_qt5_plugindir}/imageformats/libqico.so
%{_qt5_plugindir}/imageformats/libqjpeg.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGifPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QICOPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QJpegPlugin.cmake
%{_qt5_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_qt5_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QIbusPlatformInputContextPlugin.cmake
%if 0%{?egl}
%{_qt5_libdir}/libQt5EglFSDeviceIntegration.so.5*
%{_qt5_libdir}/libQt5EglFsKmsSupport.so.5*
%{_qt5_plugindir}/platforms/libqeglfs.so
%{_qt5_plugindir}/platforms/libqminimalegl.so
%dir %{_qt5_plugindir}/egldeviceintegrations/
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-integration.so
#%%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-x11-integration.so
#%%{_qt5_plugindir}/xcbglintegrations/libqxcb-egl-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-emu-integration.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalEglIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
#%%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSX11IntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsGbmIntegrationPlugin.cmake
#%%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbEglIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsEglDeviceIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSEmulatorIntegrationPlugin.cmake
%endif
%{_qt5_plugindir}/platforms/libqlinuxfb.so
%{_qt5_plugindir}/platforms/libqminimal.so
%{_qt5_plugindir}/platforms/libqoffscreen.so
%{_qt5_plugindir}/platforms/libqxcb.so
%{_qt5_plugindir}/platforms/libqvnc.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLinuxFbIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QVncIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbIntegrationPlugin.cmake
%{_qt5_plugindir}/xcbglintegrations/libqxcb-glx-integration.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbGlxIntegrationPlugin.cmake
%{_qt5_plugindir}/platformthemes/libqxdgdesktopportal.so
%{_qt5_plugindir}/platformthemes/libqgtk3.so
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXdgDesktopPortalThemePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGtk3ThemePlugin.cmake
%{_qt5_plugindir}/printsupport/libcupsprintersupport.so
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake


%changelog
* Thu Jul 13 2023 yoo <sunyuechi@iscas.ac.cn> - 5.15.2-7
- fix clang build error

* Fri Apr 28 2023 douyan <douyan@kylinos.cn> - 5.15.2-6
- fix CVE-2023-24607

* Mon Dec 12 2022 huajingyun <huajingyun@loongson.cn> - 5.15.2-5
- add loongarch64 support

* Tue Oct 25 2022 wuzx<wuzx1226@qq.com> - 5.15.2-4
- Add sw64 architecture

* Wed Jul 27 2022 peijiankang <peijiankang@kylinos.cn> - 5.15.2-3
- remove unnecessary file

* Tue Jul 26 2022 wangkai <wangkai385@h-partners.com> - 5.15.2-2
- Fix CVE-2021-38593 and CVE-2022-25255

* Sat Dec 11 2021 hua_yadong <huayadong@kylinos.cn> - 5.15.2-1
- update to upstream version 5.15.2

* Wed Apr 21 2021 wangyue <wangyue@huawei.com> - 5.11.1-14
- fix CVE-2019-18281

* Sat Nov 28 2020 liyuanrong <liyuanrong1@huawei.com> - 5.11.1-13
- add double conversion support riscv

* Mon Sep 21 2020 wutao <wutao61@huawei.com> - 5.11.1-12
- fix CVE-2015-9541

* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-11
- Fix Source0 

* Mon May 25 2020 lizhenhua <lizhenhua12@huawei.com> - 5.11.1-10
- Fix compile issue with gcc 9

* Wed Dec 25 2019 fengbing <fengbing7@huawei.com> - 5.11.1-9
- Type:cves
- ID:CVE-2018-15518
- SUG:restart
- DESC: fix CVE-2018-15518

* Thu Nov 07 2019 yanzhihua <yanzhihua4@huawei.com> - 5.11.1-8
- Package init
