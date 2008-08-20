Summary:	ConsoleKit for PolicyKit
Summary(pl.UTF-8):	ConsoleKit dla PolicyKit
Name:		ConsoleKit
Version:	0.2.10
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://people.freedesktop.org/~mccann/dist/%{name}-%{version}.tar.gz
# Source0-md5:	b85c2333a8fe31c0d3f29caa14716634
URL:		http://www.freedesktop.org/wiki/Software/ConsoleKit
BuildRequires:	PolicyKit-devel >= 0.7
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.7
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	glib2-devel >= 1:2.8.0
# for <sys/inotify.h>
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	libtool >= 1.4
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel >= 1.0.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib >= 0.30
Requires:	glib2 >= 1:2.8.0
Requires:	rc-scripts
Requires:	xorg-lib-libX11 >= 1.0.0
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
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pam-module \
	--enable-docbook-docs \
	--enable-static \
	--with-pam-module-dir=/%{_lib}/security \
	--with-pid-file=/var/run/console-kit-daemon.pid
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
%dir %{_libdir}/ConsoleKit
%dir %{_libdir}/ConsoleKit/run-session.d
%dir %{_libdir}/ConsoleKit/scripts
%attr(755,root,root) %{_libdir}/ConsoleKit/scripts/*
%attr(755,root,root) /%{_lib}/security/pam_ck_connector.so
%{_datadir}/PolicyKit/policy/ConsoleKit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ConsoleKit.service
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%dir %{_sysconfdir}/ConsoleKit
%dir %{_sysconfdir}/ConsoleKit/run-session.d
%dir %{_sysconfdir}/ConsoleKit/seats.d
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_mandir}/man8/pam_ck_connector*
%dir /var/run/ConsoleKit
%attr(750,root,root) %dir /var/log/ConsoleKit
%dir %{_localstatedir}/log/ConsoleKit

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libck-connector.so.0

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
