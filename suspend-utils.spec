#
%bcond_with	splashy
%bcond_without	initrd		# don't build resume-initrd
%bcond_without	dietlibc	# link initrd version with static glibc
#

# no-can-link splashy with dietlibc
%if %{with splashy}
%undefine with_dietlibc
%endif

%define		snap	20100118
Summary:	Suspend to RAM/Disk/Both
Summary(de.UTF-8):	Einfrieren in den Systemspeicher
Summary(pl.UTF-8):	Zamrażanie w RAM/Dysku/Jedno i drugie
Name:		suspend
Version:	0.8
Release:	0.%{snap}.1
License:	GPL v2
Group:		Applications/System
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/rafael/suspend-utils.git
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	a4bc7b06acd4f87363efcf66e7607c06
Patch0:		%{name}-sys-file-range-write.patch
Patch1:		%{name}-fadvise.patch
Patch2:		%{name}-diet.patch
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with initrd}
%{?with_dietlibc:BuildRequires:	dietlibc-static}
%endif
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

%package initrd
Summary:	Suspend to RAM/Disk/Both resume program for initrd
Summary(pl.UTF-8):	Zamrażanie w RAM/Dysku/Jedno i drugie - program resume dla initrd
Group:		Base

%description initrd
Suspend to RAM/Disk/Both resume program for initrd.

%description initrd -l pl.UTF-8
Zamrażanie w RAM/Dysku/Jedno i drugie - program resume dla initrd.

%prep
%setup -q -n %{name}-utils
%patch0 -p1
%patch1 -p2
%patch2 -p1

cat >syscalltest.c <<EOF
#include <stdio.h>
#include <sys/syscall.h>
int main() { printf("%d", SYS_reboot); return 0; }
EOF
gcc syscalltest.c -o syscalltest
SYS_REBOOT_NR=`./syscalltest`

sed -i -e "s/SYS_REBOOT_NR/$SYS_REBOOT_NR/" swsusp.h

# I don't see any issue here (nor libgcc_s.a)
%{?with_splashy:sed -i -e 's|AC_CHECK_LIB(\[gcc_s\], \[strlen\])||' configure.ac}

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

%if %{with initrd}
%configure \
	%{?with_dietlibc:CFLAGS="%{rpmcflags} -D_BSD_SOURCE -Os -static"} \
	%{?with_dietlibc:CC="diet %{__cc}"} \
	%{?with_splashy:--enable-splashy} \
	--enable-compress \
	--enable-encrypt \
	--enable-static \
	--disable-shared

%if %{with dietlibc}
%{__make} libsuspend-common.a resume-resume.o
diet %{__cc} %{rpmcflags} %{rpmldflags} -D_BSD_SOURCE -Os -static \
	-DS2RAM -D_LARGEFILE64_SOURCE -D_GNU_SOURCE \
	-o resume resume-resume.o \
	libsuspend-common.a -llzo2 -lgcrypt -lgpg-error -lcompat
%else
%{__make} resume
%endif
mv resume resume-initrd
%{__make} clean
%endif

%configure \
	%{?with_splashy:--enable-splashy} \
	--enable-compress \
	--enable-encrypt

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install resume-initrd $RPM_BUILD_ROOT%{_libdir}/initrd/resume
%endif

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

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/resume
%endif
