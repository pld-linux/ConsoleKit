Summary:	ConsoleKit for PolicyKit
Summary(pl.UTF-8):	ConsoleKit dla PolicyKit
Name:		ConsoleKit
Version:	0.2.1
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://people.freedesktop.org/~mccann/dist/%{name}-%{version}.tar.gz
# Source0-md5:	8bf5e83931a8a3c2abcd541781e1554c
Source1:	%{name}.init
Patch0:		%{name}-SIGINT.patch
URL:		http://gitweb.freedesktop.org/?p=ConsoleKit.git
BuildRequires:	PolicyKit-devel
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.7
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	glib2-devel >= 1:2.8.0
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libtool >= 1.4
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	PolicyKit
Requires:	dbus-glib >= 0.30
Requires:	glib2 >= 1:2.8.0
Requires:	rc-scripts
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
%patch0 -p1

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
	--with-pam-module-dir=/%{_lib}/security
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ConsoleKit

rm -f $RPM_BUILD_ROOT/%{_lib}/security/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ConsoleKit
%service ConsoleKit restart

%preun
if [ "$1" = "0" ]; then
	%service -q ConsoleKit stop
	/sbin/chkconfig --del ConsoleKit
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ck-list-sessions
%attr(755,root,root) %{_sbindir}/console-kit-daemon
%attr(755,root,root) %{_libdir}/ck-collect-session-info
%attr(755,root,root) %{_libdir}/ck-get-x11-server-pid
%attr(755,root,root) /%{_lib}/security/pam_ck_connector.so
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man8/pam_ck_connector*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so.*.*.*

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
