Summary:	ConsoleKit for PolicyKit
Summary(pl.UTF-8):	ConsoleKit dla PolicyKit
Name:		ConsoleKit
Version:	0.4.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://www.freedesktop.org/software/ConsoleKit/dist/%{name}-%{version}.tar.bz2
# Source0-md5:	285acb35bfcb2b8dc21c6071e6f6e116
URL:		http://www.freedesktop.org/wiki/Software/ConsoleKit
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.8.0
# for <sys/inotify.h>
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	libtool >= 1.4
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.92
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel >= 1.0.0
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-dirs = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib >= 0.30
Requires:	filesystem >= 3.0-25
Requires:	glib2 >= 1:2.8.0
Requires:	rc-scripts
Requires:	xorg-lib-libX11 >= 1.0.0
Suggests:	udev-acl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ConsoleKit is a framework for defining and tracking users, login
sessions, and seats.

%description -l pl.UTF-8
ConsoleKit to szkielet do definiowania i śledzenia użytkowników, sesji
logowania i siedzib.

%package libs
Summary:	ConsoleKit library
Summary(pl.UTF-8):	Biblioteka ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Libraries
Requires:	dbus-libs >= 0.30
Conflicts:	ConsoleKit < 0.1-0.20061203.6

%description libs
ConsoleKit library.

%description libs -l pl.UTF-8
Biblioteka ConsoleKit.

%package dirs
Summary:	ConsoleKit directories
Summary(pl.UTF-8):	Katalogi ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Libraries
Conflicts:	ConsoleKit < 0.4.1-2

%description dirs
ConsoleKit directories.

%description dirs -l pl.UTF-8
Katalogi ConsoleKit.

%package devel
Summary:	Header files for ConsoleKit
Summary(pl.UTF-8):	Pliki nagłówkowe ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 0.30

%description devel
Header files for ConsoleKit.

%description devel -l pl.UTF-8
Pliki nagłówkowe ConsoleKit.

%package static
Summary:	Static ConsoleKit library
Summary(pl.UTF-8):	Statyczna biblioteka ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ConsoleKit library.

%description static -l pl.UTF-8
Statyczna biblioteka ConsoleKit.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--enable-docbook-docs \
	--enable-pam-module \
	--enable-static \
	--with-pam-module-dir=/%{_lib}/security \
	--with-pid-file=%{_localstatedir}/run/console-kit-daemon.pid

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_lib}/security/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

# use triggerun not triggerpostun - old init script is needed to stop service
%triggerun -- ConsoleKit < 0.2.4
%service -q ConsoleKit stop
/sbin/chkconfig --del ConsoleKit

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ck-history
%attr(755,root,root) %{_bindir}/ck-launch-session
%attr(755,root,root) %{_bindir}/ck-list-sessions
%attr(755,root,root) %{_sbindir}/ck-log-system-restart
%attr(755,root,root) %{_sbindir}/ck-log-system-start
%attr(755,root,root) %{_sbindir}/ck-log-system-stop
%attr(755,root,root) %{_sbindir}/console-kit-daemon
%attr(755,root,root) %{_libdir}/ck-collect-session-info
%attr(755,root,root) %{_libdir}/ck-get-x11-server-pid
%attr(755,root,root) %{_libdir}/ck-get-x11-display-device
%attr(755,root,root) %{_prefix}/lib/ConsoleKit/scripts/*
%attr(755,root,root) /%{_lib}/security/pam_ck_connector.so
%{_datadir}/polkit-1/actions/org.freedesktop.consolekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ConsoleKit.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Seat.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Session.xml
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_mandir}/man8/pam_ck_connector.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libck-connector.so.0

%files dirs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/ConsoleKit
%dir %{_sysconfdir}/ConsoleKit/run-session.d
%dir %{_sysconfdir}/ConsoleKit/run-seat.d
%dir %{_sysconfdir}/ConsoleKit/seats.d
%dir %{_prefix}/lib/ConsoleKit/run-session.d
%dir %{_prefix}/lib/ConsoleKit/run-seat.d
%dir %{_prefix}/lib/ConsoleKit/scripts
%dir %{_localstatedir}/run/ConsoleKit
%dir %{_localstatedir}/log/ConsoleKit

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so
%{_libdir}/libck-connector.la
%dir %{_includedir}/ConsoleKit
%dir %{_includedir}/ConsoleKit/ck-connector
%{_includedir}/ConsoleKit/ck-connector/*.h
%{_pkgconfigdir}/ck-connector.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libck-connector.a
