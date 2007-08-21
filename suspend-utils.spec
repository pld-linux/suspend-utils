%define	suspend_cpu	%(echo %{_target_cpu} | sed -e s/i.86/x86/ -e s/ppc.*/ppc/ -e s/x86_64/x86/ -e s/amd64/x86/ -e s/athlon/x86/)
#
%bcond_with	splashy
#
%define	snap	20070821
Summary:	Suspend to RAM/Disk/Both
Summary(de.UTF-8):	Einfrieren in den Systemspeicher
Summary(pl.UTF-8):	Zamrażanie w RAM/Dysku/Jedno i drugie
Name:		suspend
Version:	0.6
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	4e06cd1d5fd0e5e4b1a0ffa476ce5c41
Patch0:		%{name}-sys-file-range-write.patch
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	glibc-static
BuildRequires:	libgcrypt-static
BuildRequires:	libgpg-error-static
BuildRequires:	lzo-static >= 2.02
%ifarch %{ix86} %{x8664}
BuildRequires:	libx86-static
%endif
BuildRequires:	pciutils-devel
BuildRequires:	sed >= 4.0
%if %{with splashy}
BuildRequires:	libjpeg-static
BuildRequires:	freetype-static
BuildRequires:	libpng-static
BuildRequires:	DirectFB-static
BuildRequires:	splashy-static
%endif
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%{__make} \
	CONFIG_COMPRESS=yes \
	CONFIG_ENCRYPT=yes \
	%{?with_splashy:CONFIG_SPLASHY=yes} \
	CC="%{__cc}" \
	ARCH="%{suspend_cpu}" \
	CFLAGS="%{rpmcflags}" \
	LD_FLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}

install resume s2both s2disk s2ram suspend-keygen swap-offset $RPM_BUILD_ROOT%{_sbindir}
install conf/suspend.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO README* TODO
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/suspend.conf
