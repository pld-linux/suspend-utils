%define	snap	20060325
Summary:	Suspend to RAM
Summary(pl):	Zamra¿anie w RAM
Name:		suspend
Version:	0.1
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://ep09.pld-linux.org/~arekm/%{name}-%{snap}.tar.gz
# Source0-md5:	a7b6336cce2c72cf7a7c36bfa2b24d0f
Patch0:		%{name}-whitelist.patch
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	glibc-static
BuildRequires:	liblzf-static
BuildRequires:	pciutils-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Userland parts needed for suspend-to-disk and suspend-to-RAM on Linux.

%description -l pl
Elementy przestrzeni u¿ytkownika potrzebne do zamra¿ania stanu systemu
na dysku lub w pamiêci RAM pod Linuksem.

%prep
%setup -q -n %{name}
%patch0 -p1
sed -i -e 's#gcc#%{__cc}#g' Makefile

%build
sed -i -e "s#PAGE_SIZE#$(%{_bindir}/getconf PAGE_SIZE)#g" *.c *.h
%{__make} \
	CC_FLAGS="%{rpmcflags} -DCONFIG_COMPRESS" \
	LD_FLAGS="%{rpmldflags} -llzf"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

install resume s2ram suspend $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO README TODO
%attr(755,root,root) %{_sbindir}/*
