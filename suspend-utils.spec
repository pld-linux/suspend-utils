%define	snap	20060409
Summary:	Suspend to RAM
Summary(de):	Einfrieren in den Systemspeicher (RAM)
Summary(pl):	Zamra¿anie w RAM
Name:		suspend
Version:	0.1
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://ep09.pld-linux.org/~arekm/%{name}-%{snap}.tar.gz
# Source0-md5:	7ac86007bde8d2571a25b71acd5d6d73
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	glibc-static
BuildRequires:	liblzf-static
BuildRequires:	pciutils-devel
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Userland parts needed for suspend-to-disk and suspend-to-RAM on Linux.

%description -l de
Elemente der Benutzerumgebung zum einfrieren in den Systemspeicher
oder auf die Festplatte.

%description -l pl
Elementy przestrzeni u¿ytkownika potrzebne do zamra¿ania stanu systemu
na dysku lub w pamiêci RAM pod Linuksem.

%prep
%setup -q -n %{name}

%build
%{__make} \
	CC="%{__cc}" \
	ARCH="%{_target_cpu}" \
	CC_FLAGS="%{rpmcflags} -DCONFIG_COMPRESS" \
	LD_FLAGS="%{rpmldflags} -llzf"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}

install resume s2ram suspend $RPM_BUILD_ROOT%{_sbindir}
install conf/suspend.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO README TODO
%attr(755,root,root) %{_sbindir}/*
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/suspend.conf
