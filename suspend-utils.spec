%bcond_with	splashy
#
%define	snap	20070205
Summary:	Suspend to RAM
Summary(de.UTF-8):	Einfrieren in den Systemspeicher (RAM)
Summary(pl.UTF-8):	Zamrażanie w RAM
Name:		suspend
Version:	0.6
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	dd486bb871e8c119027733d0daa51c58
Patch0:		%{name}-build.patch
Patch1:		%{name}-sys-file-range-write.patch
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	glibc-static
BuildRequires:	libgcrypt-static
BuildRequires:	libgpg-error-static
BuildRequires:	liblzf-static
BuildRequires:	pciutils-devel
BuildRequires:	sed >= 4.0
%{?with_splashy:BuildRequires:	splashy-devel}
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} %{x8664}
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
%patch1 -p1

%build
%{__make} \
	CONFIG_COMPRESS=yes \
	CONFIG_ENCRYPT=yes \
	%{?with_splashy:CONFIG_SPLASHY=yes} \
	CC="%{__cc}" \
	ARCH="%{_target_cpu}" \
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
