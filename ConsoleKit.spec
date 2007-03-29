# TODO:
# - generally check all
%define	snap	20070314
Summary:	ConsoleKit for PolicyKit
Summary(pl.UTF-8):	ConsoleKit dla PolicyKit
Name:		ConsoleKit
Version:	0.1.3
Release:	0.%{snap}.1
License:	GPL v2
Group:		Libraries
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	b4f5ce06f5d137ea559afc0461c58a73
Source1:	%{name}.init
Patch0:		%{name}-pam64.patch
URL:		http://webcvs.freedesktop.org/hal/
BuildRequires:	PolicyKit-devel
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.7
BuildRequires:	dbus-glib-devel >= 0.30
BuildRequires:	glib2-devel >= 1:2.8.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	gtk+2-devel >= 2:2.8.0
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
I totally don't know what this does, as it has no homepage.

%description -l pl.UTF-8
Totalnie nei wiem, co ta paczka robi, bo nie ma strony domowej.

%package libs
Summary:	ConsoleKit libraries
Summary(pl.UTF-8):Biblioteki ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Libraries
Requires:	dbus-libs >= 0.30
Conflicts:	ConsoleKit < 0.1-0.20061203.6

%description libs
ConsoleKit libraries.

%description libs -l pl.UTF-8
Biblioteki ConsoleKit.

%package devel
Summary:	Header files for ConsoleKit
Summary(pl.UTF-8):Pliki nagłówkowe ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 0.30

%description devel
Header files for ConsoleKit.

%description devel -l pl.UTF-8
Pliki nagłówkowe ConsoleKit.

%package static
Summary:	Static ConsoleKit libraries
Summary(pl.UTF-8):Statyczne biblioteki ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ConsoleKit libraries.

%description static -l pl.UTF-8
Statyczne biblioteki ConsoleKit.

%prep
%setup -q -n %{name}-%{snap}
%ifarch %{x8664}
%patch0 -p1
%endif

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-pam-module \
	--enable-docbook-docs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ConsoleKit

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
%attr(755,root,root) %{_libdir}/libck-connector*.so
%{_libdir}/libck-connector.la
%dir %{_includedir}/ConsoleKit
%dir %{_includedir}/ConsoleKit/ck-connector
%{_includedir}/ConsoleKit/ck-connector/*.h
%{_pkgconfigdir}/ck-connector.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libck-connector.a
