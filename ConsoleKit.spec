Summary:	ConsoleKit for PolicyKit
Summary(pl.UTF-8):	ConsoleKit dla PolicyKit
Name:		ConsoleKit
Version:	0.4.6
Release:	4
License:	GPL v2+
Group:		Libraries
Source0:	http://www.freedesktop.org/software/ConsoleKit/dist/%{name}-%{version}.tar.xz
# Source0-md5:	611792b4d616253a5bdec9175f8b7678
Source1:	%{name}.tmpfiles
Patch0:		%{name}-gzip.patch
URL:		http://www.freedesktop.org/wiki/Software/ConsoleKit
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.22.0
# for <sys/inotify.h>
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	udev-devel
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.92
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel >= 1.0.0
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-dirs = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib >= 0.82
Requires:	filesystem >= 3.0-25
Requires:	glib2 >= 1:2.14.0
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Provides:	udev-acl = 1:182-1
Obsoletes:	ConsoleKit-systemd < 0.4.5-9
Obsoletes:	udev-acl < 1:182
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

%package x11
Summary:	X11 session support for ConsoleKit
Summary(pl.UTF-8):	Obsługa sesji X11 dla pakietu ConsoleKit
License:	GPL v2+
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libX11 >= 1.0.0

%description x11
X11 session support utilities for ConsoleKit.

%description x11 -l pl.UTF-8
Narzędzia obsługujące sesje X11 dla pakietu ConsoleKit.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules \
	--enable-docbook-docs \
	--enable-pam-module \
	--enable-static \
	--with-pam-module-dir=/%{_lib}/security \
	--with-pid-file=%{_localstatedir}/run/console-kit-daemon.pid \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--enable-udev-acl

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

# loadable module
%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/*.{a,la}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libck-connector.la

%clean
rm -rf $RPM_BUILD_ROOT

# use triggerun not triggerpostun - old init script is needed to stop service
%triggerun -- ConsoleKit < 0.2.4
%service -q ConsoleKit stop
/sbin/chkconfig --del ConsoleKit

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
%systemd_post console-kit-daemon.service

%preun
%systemd_preun console-kit-daemon.service

%postun
%systemd_reload

%triggerpostun -- ConsoleKit < 0.4.5-9
%systemd_trigger console-kit-daemon.service

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
%attr(755,root,root) %{_libexecdir}/ck-collect-session-info
%attr(755,root,root) %{_prefix}/lib/ConsoleKit/scripts/*
%attr(755,root,root) /%{_lib}/security/pam_ck_connector.so
%{_datadir}/polkit-1/actions/org.freedesktop.consolekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ConsoleKit.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Seat.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Session.xml
/etc/dbus-1/system.d/ConsoleKit.conf
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_mandir}/man8/pam_ck_connector.8*
%{systemdunitdir}/basic.target.wants/console-kit-log-system-start.service
%{systemdunitdir}/console-kit-daemon.service
%{systemdunitdir}/console-kit-log-system-restart.service
%{systemdunitdir}/console-kit-log-system-start.service
%{systemdunitdir}/console-kit-log-system-stop.service
%{systemdunitdir}/halt.target.wants/console-kit-log-system-stop.service
%{systemdunitdir}/kexec.target.wants/console-kit-log-system-restart.service
%{systemdunitdir}/poweroff.target.wants/console-kit-log-system-stop.service
%{systemdunitdir}/reboot.target.wants/console-kit-log-system-restart.service

%attr(755,root,root) /lib/udev/udev-acl
%attr(755,root,root) /usr/lib/ConsoleKit/run-seat.d/udev-acl.ck
/lib/udev/rules.d/70-udev-acl.rules
 
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libck-connector.so.0

%files dirs
%defattr(644,root,root,755)
%{systemdtmpfilesdir}/ConsoleKit.conf
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
%dir %{_includedir}/ConsoleKit
%{_includedir}/ConsoleKit/ck-connector
%{_pkgconfigdir}/ck-connector.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libck-connector.a

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/ck-get-x11-server-pid
%attr(755,root,root) %{_libexecdir}/ck-get-x11-display-device
