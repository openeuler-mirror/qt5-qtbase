%global __provides_exclude_from ^%{_qt5_plugindir}/.*\\.so$
%global __requires_exclude_from ^%{_qt5_plugindir}/platformthemes/.*$
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global priority 10
%ifarch x86_64
%global priority 15
%endif

%if 0%{?use_clang}
%global platform linux-clang
%endif

Name:             qt5-qtbase
Summary:          Core component of Qt toolkit
Version:          5.11.1
Release:          10
License:          LGPLv2 with exceptions or GPLv3 with exceptions
Url:              http://qt-project.org/
Source0:          https://download.qt.io/new_archive/qt/5.11/%{version}/submodules/qtbase-everywhere-src-%{version}.tar.xz
Source1:          qtlogging.ini
Source2:          qconfig-multilib.h
Source3:          10-qt5-check-opengl2.sh
Source4:          macros.qt5-qtbase

Patch0001:        qtbase-multilib_optflags.patch
Patch0002:        qtbase-opensource-src-5.3.2-QTBUG-35459.patch
Patch0003:        tell-the-truth-about-private-api.patch
Patch0004:        qtbase-opensource-src-5.8.0-QT_VERSION_CHECK.patch
Patch0005:        qtbase-hidpi_scale_at_192.patch
Patch0006:        qtbase-opensource-src-5.7.1-moc_macros.patch
Patch0007:        qtbase-qmake_LFLAGS.patch
Patch0008:        qt5-qtbase-cxxflag.patch
Patch0009:        qt5-qtbase-5.9.1-firebird.patch
Patch0010:        qtbase-everywhere-src-5.11.1-python3.patch
Patch0011:        qt5-qtbase-glibc.patch

Patch6000:        CVE-2018-15518.patch 

BuildRequires:    pkgconfig(libsystemd) cups-devel desktop-file-utils findutils
BuildRequires:    libjpeg-devel libmng-devel libtiff-devel pkgconfig(alsa)
BuildRequires:    pkgconfig(atspi-2) pkgconfig(dbus-1) pkgconfig(libdrm)
BuildRequires:    pkgconfig(fontconfig) pkgconfig(gl) pkgconfig(glib-2.0)
BuildRequires:    pkgconfig(gtk+-3.0) pkgconfig(libproxy-1.0) pkgconfig(ice) pkgconfig(sm)
BuildRequires:    pkgconfig(libpng) pkgconfig(libudev) openssl-devel%{?openssl11: >= 1.1}
BuildRequires:    pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires:    pkgconfig(xkeyboard-config) pkgconfig(egl) pkgconfig(gbm) pkgconfig(glesv2)
BuildRequires:    pkgconfig(sqlite3) >= 3.7 pkgconfig(icu-i18n) pkgconfig(libpcre2-posix) >= 10.20
BuildRequires:    pkgconfig(libpcre) >= 8.0 pkgconfig(xcb-xkb) pkgconfig(xcb) pkgconfig(xcb-glx)
BuildRequires:    pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms)
BuildRequires:    pkgconfig(xcb-renderutil) pkgconfig(zlib) perl-generators qt5-rpm-macros

%if 0%{?use_clang}
BuildRequires:    clang >= 3.7.0
%else
BuildRequires:    gcc-c++
%endif

%if 0%{?tests}
BuildRequires:    dbus-x11 mesa-dri-drivers time xorg-x11-server-Xvfb
%endif

%if 0%{?use_clang}
BuildRequires:    clang >= 3.7.0
%else
BuildRequires:    gcc-c++
%endif

Requires(post):   chkconfig
Requires(postun): chkconfig
Requires:         qt-settings %{name}-common = %{version}-%{release}
Provides:         bundled(libxkbcommon) = 0.4.1

%description
This package provides base tools, such as string, xml, and network
handling.

%package common
Summary:          Common files for qt5-qtbase
Obsoletes:        qt5-qtquick1 < 5.9.0 qt5-qtquick1-devel < 5.9.0
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch
%description common
The qt5-qtbase-common package contains common files for qt5-qtbase.

%package devel
Summary:          Library and header files for qt5-qtbase
Requires:         %{name} = %{version}-%{release} %{name}-gui pkgconfig(egl) pkgconfig(gl)
Requires:         qt5-rpm-macros pkgconfig(fontconfig) pkgconfig(glib-2.0) pkgconfig(zlib)
%if 0%{?use_clang}
Requires: clang >= 3.7.0
%endif
Provides:         %{name}-private-devel = %{version}-%{release}
Provides:         %{name}-static = %{version}-%{release} %{name}-examples = %{version}-%{release}
Obsoletes:        %{name}-static < %{version}-%{release} %{name}-examples < %{version}-%{release}
%description devel
The qt5-qtbase-devel contains libraries and header files for qt5-qtbase.

%package mysql
Summary:          MySQL driver for Qt5's SQL classes
BuildRequires:    mysql-devel
Requires:         %{name} = %{version}-%{release}
%description mysql
Qt5-qtbase-mysql provides MySQL driver for Qt5's SQL classes.

%package odbc
Summary:          ODBC driver for Qt5's SQL classes
BuildRequires:    unixODBC-devel
Requires:         %{name} = %{version}-%{release}
%description odbc
Qt5-qtbase-odbc provides ODBC driver for Qt5's SQL classes.

%package postgresql
Summary:          PostgreSQL driver for Qt5's SQL classes
BuildRequires:    postgresql-devel
Requires:         %{name} = %{version}-%{release}
%description postgresql
Qt5-qtbase-postgresql provides postgreSQL driver for Qt5's SQL classes.


%package gui
Summary:         Qt5 GUI-related libraries
Requires:        %{name} = %{version}-%{release} glx-utils
Provides:        qt5-qtbase-x11 = %{version}-%{release}
Obsoletes:       qt5-qtbase-x11 < 5.2.0
%description gui
qt5-qtbase-gui is a library helps to draw widgets and OpenGL items with.

%prep
%autosetup -n qtbase-everywhere-src-%{version} -p1

pushd src/3rdparty
mkdir UNUSED
mv freetype libjpeg libpng zlib sqlite xcb UNUSED/
popd

test -x configure || chmod +x configure

sed -i -e "s|^#!/usr/bin/env perl$|#!%{__perl}|" \
    bin/fixqt4headers.pl bin/syncqt.pl mkspecs/features/data/unix/findclasslist.pl


%build
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`
RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?qt5_arm_flag} %{?qt5_deprecated_flag} %{?qt5_null_flag}"

%if 0%{?use_clang}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fno-delete-null-pointer-checks||g'`
%endif

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS" CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS" MAKEFLAGS="%{?_smp_mflags}"

./configure -verbose -confirm-license -opensource -prefix %{_qt5_prefix} \
  -archdatadir %{_qt5_archdatadir} -bindir %{_qt5_bindir} -libdir %{_qt5_libdir} \
  -libexecdir %{_qt5_libexecdir} -datadir %{_qt5_datadir} -docdir %{_qt5_docdir} \
  -examplesdir %{_qt5_examplesdir} -headerdir %{_qt5_headerdir} -importdir %{_qt5_importdir} \
  -plugindir %{_qt5_plugindir} -sysconfdir %{_qt5_sysconfdir} -translationdir %{_qt5_translationdir} \
  -platform linux-g++ -release -shared -accessibility -dbus-linked -fontconfig -glib -gtk \
  -no-sql-ibase -icu -journald -optimized-qmake -openssl-linked %{!?tests:-nomake tests} -no-pch \
  -no-rpath -no-separate-debug-info -no-strip -system-libjpeg -system-libpng %{?harfbuzz} -system-pcre \
  -system-sqlite -no-sql-tds %{?xcb} -qt-xkbcommon -system-zlib %{?use_gold_linker} -no-directfb \
  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}"

make clean -C qmake
%make_build -C qmake all binary QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS:-$RPM_OPT_FLAGS}" \
  QMAKE_CFLAGS_RELEASE="${CFLAGS:-$RPM_OPT_FLAGS}" QMAKE_LFLAGS_RELEASE="${LDFLAGS:-$RPM_LD_FLAGS}" QMAKE_STRIP=

%make_build

%install
make install INSTALL_ROOT=%{buildroot}

install -m644 -p -D %{SOURCE1} %{buildroot}%{_qt5_datadir}/qtlogging.ini

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
Version: %{version}
EOF

install -p -m644 -D %{SOURCE4} %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase
sed -i -e "s|@@NAME@@|%{name}|g;s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
    -e "s|@@VERSION@@|%{version}|g;s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
    %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase

install -d %{buildroot}{%{_qt5_archdatadir}/mkspecs/modules,%{_qt5_importdir},%{_qt5_libexecdir}}
install -d %{buildroot}{%{_qt5_plugindir}/{designer,iconengines,script,styles},%{_qt5_translationdir}}
install -d %{buildroot}{%{_sysconfdir}/xdg/QtProject,%{_bindir}}
pushd %{buildroot}%{_qt5_bindir}
for file in * ; do
  case "${file}" in
    moc|qdbuscpp2xml|qdbusxml2cpp|qmake|rcc|syncqt|uic)
      ln -v  ${file} %{buildroot}%{_bindir}/${file}-qt5
      ln -sv ${file} ${file}-qt5
      ;;
    *)
      ln -v  ${file} %{buildroot}%{_bindir}/${file}
      ;;
  esac
done
popd

%ifarch x86_64
  pushd %{buildroot}%{_qt5_headerdir}/QtCore
  mv qconfig.h qconfig-%{__isa_bits}.h
  popd
  install -p -m644 -D %{SOURCE2} %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h
%endif

install -d %{buildroot}%{_sysconfdir}/xdg/qtchooser
pushd      %{buildroot}%{_sysconfdir}/xdg/qtchooser
echo "%{_qt5_bindir}" >  5-%{__isa_bits}.conf
echo "%{_qt5_prefix}" >> 5-%{__isa_bits}.conf
touch default.conf 5.conf
popd

pushd %{buildroot}%{_qt5_libdir}
for file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${file}
  if [ -f "$(basename ${file} .prl).so" ]; then
    rm -fv "$(basename ${file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${file}
  fi
done
popd

install -p -m755 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh

privat_header_file=%{buildroot}%{_qt5_headerdir}/QtCore/%{version}/QtCore/private/qconfig_p.h
grep -v QT_FEATURE_sse2 $privat_header_file > ${privat_header_file}.me
mv ${privat_header_file}.me ${privat_header_file}
cat >>${privat_header_file}<<EOF
EOF

install -d %{buildroot}%{_qt5_headerdir}/QtXcb
install -m644 src/plugins/platforms/xcb/*.h %{buildroot}%{_qt5_headerdir}/QtXcb/

%check
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion Qt5)" = "%{version}"
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1 PATH=%{buildroot}%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
dbus-launch --exit-with-session %make_build sub-tests  -k ||:
xvfb-run -a --server-args="-screen 0 1280x1024x32" \
dbus-launch --exit-with-session time make check -k ||:
%endif


%pre
if [ $1 -gt 1 ] ; then
%{_sbindir}/update-alternatives --remove qtchooser-qt5 \
  %{_sysconfdir}/xdg/qtchooser/qt5-%{__isa_bits}.conf >& /dev/null ||:

%{_sbindir}/update-alternatives --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/qt5.conf >& /dev/null ||:
fi

%post
%{?ldconfig}
%{_sbindir}/update-alternatives --install %{_sysconfdir}/xdg/qtchooser/5.conf \
  qtchooser-5 %{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf %{priority}

%{_sbindir}/update-alternatives --install %{_sysconfdir}/xdg/qtchooser/default.conf \
  qtchooser-default %{_sysconfdir}/xdg/qtchooser/5.conf %{priority}

%postun
%{?ldconfig}
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives --remove qtchooser-5 \
  %{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf

%{_sbindir}/update-alternatives --remove qtchooser-default \
  %{_sysconfdir}/xdg/qtchooser/5.conf
fi

%files
%license LICENSE.LGPL* LGPL_EXCEPTION.txt LICENSE.FDL
%dir %{_sysconfdir}/xdg/qtchooser
%ghost %{_sysconfdir}/xdg/qtchooser/default.conf
%ghost %{_sysconfdir}/xdg/qtchooser/5.conf
%{_sysconfdir}/xdg/qtchooser/5-%{__isa_bits}.conf
%dir %{_qt5_docdir}/
%dir %{_qt5_datadir}/
%dir %{_qt5_archdatadir}/
%dir %{_qt5_libexecdir}/
%dir %{_sysconfdir}/xdg/QtProject/
%dir %{_qt5_libdir}/cmake/{Qt5/,Qt5Concurrent/,Qt5Core/,Qt5DBus/,Qt5Gui/}
%dir %{_qt5_libdir}/cmake/{Qt5Network/,Qt5OpenGL/,Qt5PrintSupport/,Qt5Sql/}
%dir %{_qt5_libdir}/cmake/{Qt5Test/,Qt5Widgets/,Qt5Xml/}
%dir %{_qt5_plugindir}/{designer/,generic/,iconengines/,imageformats/}
%dir %{_qt5_plugindir}/{platforminputcontexts/,platforms/,platformthemes/}
%dir %{_qt5_plugindir}/{printsupport/,script/,sqldrivers/,styles/,bearer/}
%if "%{_qt5_prefix}" != "%{_prefix}"
%dir %{_qt5_prefix}/
%endif
%{_qt5_docdir}/global/
%{_qt5_importdir}/
%{_qt5_translationdir}/
%{_qt5_datadir}/qtlogging.ini
%{_qt5_plugindir}/sqldrivers/libqsqlite.so
%{_qt5_plugindir}/bearer/{libqconnmanbearer,libqgenericbearer,libqnmbearer}.so
%{_qt5_libdir}/{libQt5Concurrent,libQt5Core,libQt5DBus,libQt5Network}.so.5*
%{_qt5_libdir}/{libQt5Sql,libQt5Test,libQt5Xml}.so.5*
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5Network_Q*EnginePlugin.cmake

%files common
%{rpm_macros_dir}/macros.qt5-qtbase

%files devel
%if "%{_qt5_bindir}" != "%{_bindir}"
%dir %{_qt5_bindir}
%endif
%if "%{_qt5_headerdir}" != "%{_includedir}"
%dir %{_qt5_headerdir}
%endif
%{_bindir}/{qlalr,fixqt4headers.pl,qvkgen}
%{_bindir}/{moc*,qdbuscpp2xml*,qdbusxml2cpp*,qmake*,rcc*,syncqt*,uic*}
%{_qt5_bindir}/{moc*,qdbuscpp2xml*,qdbusxml2cpp*,qmake*,rcc*}
%{_qt5_bindir}/{syncqt*,uic*,qlalr,fixqt4headers.pl,qvkgen}
%{_qt5_headerdir}/Qt*Support
%{_qt5_headerdir}/{QtConcurrent/,QtCore/,QtDBus/,QtGui/,QtNetwork/,QtOpenGL/,QtOpenGLExtensions/}
%{_qt5_headerdir}/{QtPlatformHeaders/,QtSql/,QtTest/,QtWidgets/}
%{_qt5_headerdir}/{QtXcb/,QtXml/,QtEglFSDeviceIntegration}
%{_qt5_archdatadir}/mkspecs/
%{_qt5_libdir}/libQt5*.{so,*a,prl}
%{_qt5_libdir}/cmake/Qt5/{Qt5Config*,Qt5ModuleLocation}.cmake
%{_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_qt5_libdir}/cmake/Qt5Concurrent/Qt5ConcurrentConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Core/{Qt5CoreConfig*,Qt5CoreMacros,Qt5CTestMacros}.cmake
%{_qt5_libdir}/cmake/Qt5DBus/{Qt5DBusConfig*,Qt5DBusMacros}.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%{_qt5_libdir}/cmake/Qt5OpenGL/Qt5OpenGLConfig*.cmake
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Test/Qt5TestConfig*.cmake
%{_qt5_libdir}/cmake/Qt5Widgets/{Qt5WidgetsConfig*,Qt5WidgetsMacros}.cmake
%{_qt5_libdir}/cmake/Qt5Xml/Qt5XmlConfig*.cmake
%{_qt5_libdir}/pkgconfig/Qt5*.pc
%{_qt5_libdir}/libQt5EglFsKmsSupport.{prl,so}
%{_qt5_examplesdir}/

%files mysql
%{_qt5_plugindir}/sqldrivers/libqsqlmysql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QMYSQLDriverPlugin.cmake

%files odbc
%{_qt5_plugindir}/sqldrivers/libqsqlodbc.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QODBCDriverPlugin.cmake

%files postgresql
%{_qt5_plugindir}/sqldrivers/libqsqlpsql.so
%{_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QPSQLDriverPlugin.cmake


%post gui -p /sbin/ldconfig
%postun gui -p /sbin/ldconfig

%files gui
%dir %{_sysconfdir}/X11/xinit/xinitrc.d/
%dir %{_qt5_plugindir}/egldeviceintegrations/
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%{_qt5_libdir}/{libQt5Gui,libQt5OpenGL,libQt5PrintSupport,libQt5Widgets,libQt5XcbQpa}.so.5*
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_Q*Plugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_Q*PlatformInputContextPlugin.cmake
%{_qt5_libdir}/{libQt5EglFSDeviceIntegration,libQt5EglFsKmsSupport}.so.5*
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_Q*IntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_Q*ThemePlugin.cmake
%{_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbGlxIntegrationPlugin.cmake
%{_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake
%{_qt5_plugindir}/generic/{libqevdev*plugin,libqtuiotouchplugin}.so
%{_qt5_plugindir}/imageformats/{libqgif,libqico,libqjpeg}.so
%{_qt5_plugindir}/platforminputcontexts/lib*platforminputcontextplugin.so
%{_qt5_plugindir}/platforms/{libqeglfs,libqminimalegl}.so
%{_qt5_plugindir}/xcbglintegrations/libqxcb-*-integration.so
%{_qt5_plugindir}/egldeviceintegrations/libqeglfs-*-integration.so
%{_qt5_plugindir}/platforms/{libqlinuxfb,libqminimal,libqoffscreen,libqxcb,libqvnc}.so
%{_qt5_plugindir}/platformthemes/{libqflatpak,libqgtk3}.so
%{_qt5_plugindir}/printsupport/libcupsprintersupport.so


%changelog
* Fri Sep 18 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-10
- Fix Source0 

* Wed Dec 25 2019 fengbing <fengbing7@huawei.com> - 5.11.1-9
- Type:cves
- ID:CVE-2018-15518
- SUG:restart
- DESC: fix CVE-2018-15518


* Thu Nov 07 2019 yanzhihua <yanzhihua4@huawei.com> - 5.11.1-8
- Package init
