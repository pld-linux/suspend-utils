#
%bcond_with	splashy
#
%define	snap	20071028
Summary:	Suspend to RAM/Disk/Both
Summary(de.UTF-8):	Einfrieren in den Systemspeicher
Summary(pl.UTF-8):	Zamrażanie w RAM/Dysku/Jedno i drugie
Name:		suspend
Version:	0.8
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	7ab0f6db95e3fe0b0e52213fa415623a
Patch0:		%{name}-sys-file-range-write.patch
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glibc-static
BuildRequires:	libgcrypt-static
BuildRequires:	libgpg-error-static
BuildRequires:	libtool
BuildRequires:	lzo-static >= 2.02
%ifarch %{ix86} %{x8664}
BuildRequires:	libx86-static
%endif
BuildRequires:	pciutils-devel
BuildRequires:	sed >= 4.0
%if %{with splashy}
BuildRequires:	DirectFB-static
BuildRequires:	freetype-static
BuildRequires:	libjpeg-static
BuildRequires:	libpng-static
BuildRequires:	splashy-static
%endif
BuildRequires:	zlib-devel
Conflicts:	geninitrd < 8880
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libz for gzopen gets discarded if same cache reused (probably ac variables conflict)
%undefine	configure_cache

%description
Userland parts needed for suspend-to-disk and suspend-to-RAM on Linux.

%description -l de.UTF-8
Elemente der Benutzerumgebung zum einfrieren in den Systemspeicher
oder auf die Festplatte.

%description -l pl.UTF-8
Elementy przestrzeni użytkownika potrzebne do zamrażania stanu systemu
na dysku lub w pamięci RAM pod Linuksem.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO README* TODO
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/suspend
%attr(755,root,root) %{_libdir}/suspend/resume
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/suspend.conf
