%define	snap	20060222
Summary:	Suspend to RAM
Name:		s2ram
Version:	0.1
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	02356c96a511493e4baa6ac1949ce016
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	liblzf-static
BuildRequires:	pciutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Userland parts needed for suspend-to-disk and suspend-to-RAM on Linux.

%prep
%setup -q -n suspend

%build
sed -i -e 's#gcc#%{__cc}#g' Makefile
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
