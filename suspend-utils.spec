%define	_snap	20060807
%define	_rel	1
Summary:	Suspend to RAM
Summary(de):	Einfrieren in den Systemspeicher (RAM)
Summary(pl):	Zamra¿anie w RAM
Name:		suspend
Version:	0.2
Release:	0.%{_snap}.%{_rel}
License:	GPL v2
Group:		Applications/System
Source0:	http://ep09.pld-linux.org/~arekm/%{name}-%{_snap}.tar.gz
# Source0-md5:	c89ebdf1b25e31d05ae86c73e68c4289
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

install resume s2both s2disk s2ram $RPM_BUILD_ROOT%{_sbindir}
install conf/suspend.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO README* TODO
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/suspend.conf
