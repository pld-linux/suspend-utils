#
%bcond_with	plymouth
%bcond_with	splashy
%bcond_with	initrd		# don't build resume-initrd
%bcond_without	dietlibc	# link initrd version with static glibc
%bcond_with	encrypt		# build s2disk with image encryption support
#

# no-can-link splashy with dietlibc
%if %{with splashy}
%undefine with_dietlibc
%endif

Summary:	Suspend to RAM/Disk/Both
Summary(de.UTF-8):	Einfrieren in den Systemspeicher
Summary(pl.UTF-8):	Zamrażanie w RAM/na dysku/jedno i drugie
Name:		suspend-utils
Version:	1.0
Release:	5
License:	GPL v2
Group:		Applications/System
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/rafael/suspend-utils.git
# Source0:	%{name}-%{snap}.tar.bz2
Source0:	http://dl.sourceforge.net/project/suspend/suspend/suspend-1.0/suspend-utils-1.0.tar.bz2
# Source0-md5:	02f7d4b679bad1bb294a0efe48ce5934
Source1:	wlcsv2c.pl
Patch0:		suspend-sys-file-range-write.patch
Patch1:		suspend-fadvise.patch
Patch2:		suspend-diet.patch
Patch3:		suspend-utils-conf.patch
Patch4:		suspend-utils-build.patch
Patch5:		suspend-ignore-acpi-video-flags-not-available.patch
Patch6:		suspend-plymouth.patch
Patch7:		s2disk-do-not-fail-without-local-terminals.patch
Patch8:		s2disk-disable-splash-when-unable-to-switch-vts.patch
URL:		http://sourceforge.net/projects/suspend
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with initrd}
%{?with_dietlibc:BuildRequires:	dietlibc-static}
%endif
BuildRequires:	glibc-static
%if %{with encrypt}
BuildRequires:	libgcrypt-static
BuildRequires:	libgpg-error-static
%endif
BuildRequires:	libtool
BuildRequires:	lzo-static >= 2.02
%ifarch %{ix86} %{x8664}
BuildRequires:	libx86-static
%endif
BuildRequires:	pciutils-devel
BuildRequires:	perl-Switch
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%{?with_plymouth:BuildRequires:	plymouth-static >= 0.8.8-8}
%if %{with splashy}
BuildRequires:	DirectFB-static
BuildRequires:	freetype-static
BuildRequires:	libjpeg-static
BuildRequires:	libpng-static
BuildRequires:	splashy-static
%endif
BuildRequires:	zlib-devel
Requires:	uname(release) >= 2.6.17
Provides:	suspend = %{version}-%{release}
Obsoletes:	suspend < 1.0
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
Summary(pl.UTF-8):	Zamrażanie w RAM/na dysku/jedno i drugie - program resume dla initrd
Group:		Base
Obsoletes:	suspend-initrd < 1.0

%description initrd
Suspend to RAM/Disk/Both resume program for initrd.

%description initrd -l pl.UTF-8
Zamrażanie w RAM/Dysku/Jedno i drugie - program resume dla initrd.

%prep
%setup -q
%patch0 -p1
%patch1 -p2
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

install %{SOURCE1} .

cat >syscalltest.c <<EOF
#include <stdio.h>
#include <sys/syscall.h>
int main() { printf("%d", SYS_reboot); return 0; }
EOF
%{__cc} syscalltest.c -o syscalltest
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
__cc="%{__cc}"
__cc=${__cc#ccache }
%configure \
	%{?with_dietlibc:CFLAGS="%{rpmcflags} -D_BSD_SOURCE -Os -static"} \
	%{?with_dietlibc:CC="diet ${__cc}"} \
	%{?with_splashy:--enable-splashy} \
	%{__enable_disable encrypt} \
	--enable-compress \
	--enable-static \
	--disable-shared

%if %{with dietlibc}
%{__make} libsuspend-common.a resume-resume.o
diet ${__cc} %{rpmcflags} %{rpmldflags} -D_BSD_SOURCE -Os -static \
	-DS2RAM -D_LARGEFILE64_SOURCE -D_GNU_SOURCE \
	-o resume resume-resume.o \
	libsuspend-common.a -llzo2 %{?with_encrypt:-lgcrypt -lgpg-error} -lcompat
%else
%{__make} resume
%endif
mv resume resume-initrd
%{__make} clean
%endif

%configure \
	%{?with_splashy:--enable-splashy} \
	%{?with_plymouth:--enable-plymouth} \
	%{__enable_disable encrypt} \
	--enable-compress \
	--enable-threads \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install -p resume-initrd $RPM_BUILD_ROOT%{_libdir}/initrd/resume
%endif

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without encrypt}
%post
%banner suspend-utils -e <<EOF
Warning!
This version of suspend-utils is built without support
for encrypted s2disk images.
EOF
%endif

%files
%defattr(644,root,root,755)
%doc HOWTO README* AUTHORS ReleaseNotes
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/suspend
%attr(755,root,root) %{_libdir}/suspend/resume
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/suspend.conf

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/resume
%endif
