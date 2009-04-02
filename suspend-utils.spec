#
%bcond_with	splashy
#
%define		snap	20090403
Summary:	Suspend to RAM/Disk/Both
Summary(de.UTF-8):	Einfrieren in den Systemspeicher
Summary(pl.UTF-8):	Zamrażanie w RAM/Dysku/Jedno i drugie
Name:		suspend
Version:	0.8
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
# cvs -z3 -d:pserver:anonymous@suspend.cvs.sf.net:/cvsroot/suspend co suspend
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	91616804cabb90656daaed8a5cf1da20
Patch0:		%{name}-sys-file-range-write.patch
Patch1:		%{name}-fadvise.patch
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
Requires:	uname(release) >= 2.6.17
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
%patch1 -p2

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

%configure \
	%{?with_splashy:--enable-splashy} \
	--enable-compress \
	--enable-encrypt
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
