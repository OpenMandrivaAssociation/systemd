%bcond_with bootstrap
%ifarch %armx
%bcond_with uclibc
%else
%bcond_without uclibc
%endif

# macros for sysvinit transition - should be equal to
# sysvinit %version-%release-plus-1
%define sysvinit_version 2.87
%define sysvinit_release %mkrel 23

%define libsystemd_major 0
%define libdaemon_major 0
%define liblogin_major 0
%define libjournal_major 0
%define libid128_major 0
%define libnss_major 2

%define libsystemd %mklibname %{name} %{libsystemd_major}
%define libsystemd_devel %mklibname %{name} -d

%define libdaemon %mklibname systemd-daemon %{libdaemon_major}
%define libdaemon_devel %mklibname systemd-daemon -d

%define liblogin %mklibname systemd-login %{liblogin_major}
%define liblogin_devel %mklibname systemd-login -d

%define libjournal %mklibname systemd-journal %{libjournal_major}
%define libjournal_devel %mklibname systemd-journal -d

%define libid128 %mklibname systemd-id128 %{libid128_major}
%define libid128_devel %mklibname systemd-id128 -d

%define libnss_myhostname %mklibname nss_myhostname %{libnss_major}

%define udev_major 1
%define libudev %mklibname udev %{udev_major}
%define libudev_devel %mklibname udev -d

%define systemd_libdir /lib/systemd
%define udev_libdir /lib/udev
%define udev_rules_dir %{udev_libdir}/rules.d
%define udev_user_rules_dir %{_sysconfdir}/udev/rules.d

Summary:	A System and Session Manager
Name:		systemd
Version:	221
Release:	6
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
Source2:	50-udev-mandriva.rules
Source3:	69-printeracl.rules
Source5:	udev.sysconfig
# (blino) net rules and helpers
Source6:	76-net.rules
Source7:	udev_net_create_ifcfg
Source8:	udev_net_action
Source9:	udev_net.sysconfig
# (hk) udev rules for zte 3g modems with drakx-net
Source10:	61-mobile-zte-drakx-net.rules
Source11:	listen.conf
# (tpg) default preset for services
Source12:	99-default-disable.preset
Source13:	90-default.preset
Source14:	85-display-manager.preset
Source16:	systemd.rpmlintrc
# (tpg) by default enable network on eth, enp0s3
Source17:	90-enable.network
Source18:	90-user-default.preset
Source19:	10-imx.rules
Source20:	90-wireless.network

### OMV patches###
# from Mandriva
# disable coldplug for storage and device pci
#po 315
#Patch2:		udev-199-coldplug.patch
# We need a static libudev.a for the uClibc build because lvm2 requires it.
# Put back support for building it.
Patch4:		systemd-220-static.patch
Patch5:		systemd-216-set-udev_log-to-err.patch
# uClibc lacks secure_getenv(), DO NOT REMOVE!
Patch6:		systemd-221-support-build-without-secure_getenv.patch
Patch7:		systemd-221-uclibc-no-mkostemp.patch
Patch8:		systemd-206-set-max-journal-size-to-150M.patch
#Patch9:		systemd-208-fix-race-condition-between-udev-and-vconsole.patch
#Patch10:	systemd-214-uclibc.patch
Patch11:	systemd-220-silent-fsck-on-boot.patch
Patch13:	systemd-221-uclibc-exp10-replacement.patch
Patch14:	systemd-217-do-not-run-systemd-firstboot-in-containers.patch
Patch15:	1005-create-default-links-for-primary-cd_dvd-drive.patch
# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1092
# keep this patch until upstream will fix it
Patch16:	systemd-219-always-restart-systemd-timedated.service.patch
Patch17:	0515-Add-path-to-locale-search.patch
Patch18:	systemd-221-add-missing-signal_h-header.patch
# (tpg) prolly this will be fixed dirrefently in next release
# https://bugzilla.redhat.com/show_bug.cgi?id=1141137
Patch19:	systemd-221-revert-wait_for_exit-true.patch

# UPSTREAM GIT PATCHES

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	m4
BuildRequires:	libtool
BuildRequires:	acl-devel
BuildRequires:	audit-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	gperf
BuildRequires:	intltool
BuildRequires:	cap-devel
BuildRequires:	pam-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	tcp_wrappers-devel
BuildRequires:	vala >= 0.9
BuildRequires:	elfutils-devel
BuildRequires:	pkgconfig(dbus-1) >= 1.8.0
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	gtk-doc
%if !%{with bootstrap}
BuildRequires:	pkgconfig(libcryptsetup)
%if %{with uclibc}
BuildRequires:	uclibc-cryptsetup-devel
%endif
%endif
BuildRequires:	pkgconfig(libkmod) >= 5
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libqrencode)
BuildRequires:	pkgconfig(libiptc)
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(blkid)
BuildRequires:	usbutils >= 005-3
BuildRequires:	pciutils-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(liblz4)
%if !%{with bootstrap}
BuildRequires:	python-devel
BuildRequires:	python-lxml
BuildRequires:	python-sphinx
%endif
%ifnarch %armx
BuildRequires:	valgrind-devel
BuildRequires:	gnu-efi
BuildRequires:	qemu
%endif
BuildRequires:	chkconfig
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libidn)
#BuildRequires:	apparmor-devel
# To make sure _rundir is defined
BuildRequires:  rpm-build >= 1:5.4.10-79
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(mount)
# make sure we have /etc/os-release available, required by --with-distro
BuildRequires:	distro-release-common >= 2012.0-0.4
%if !%{with bootstrap}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%endif
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.3-0.20150520.2
BuildRequires:	uclibc-acl-devel
BuildRequires:	uclibc-bzip2-devel
BuildRequires:	uclibc-lzma-devel
BuildRequires:	uclibc-kmod-devel
BuildRequires:	uclibc-libcap-devel
BuildRequires:	uclibc-libmount-devel
BuildRequires:	uclibc-dbus-devel
%endif
Requires:	acl
Requires:	dbus >= 1.8.0
Requires(pre,post):	coreutils >= 8.23
Requires(post):	gawk
Requires(post):	awk
Requires(post):	grep
Requires(post):	awk
Requires(pre):	basesystem-minimal >= 2015.0
Requires(pre):	util-linux >= 2.26.2
Requires(pre):	shadow >= 4.2.1-11
Requires(pre,post,postun):	setup >= 2.8.8-16
Requires:	lockdev
Requires:	kmod >= 20
Conflicts:	initscripts < 9.24
Conflicts:	udev < 221-1
%if "%{distepoch}" >= "2013.0"
#(tpg) time to drop consolekit stuff as it is replaced by native logind
Provides:	consolekit = 0.4.5-6
Provides:	consolekit-x11 = 0.4.5-6
Obsoletes:	consolekit <= 0.4.5-5
Obsoletes:	consolekit-x11 <= 0.4.5-5
Obsoletes:	libconsolekit0
Obsoletes:	lib64consolekit0
%endif
%if "%{distepoch}" >= "2015.0"
# (tpg) this is obsoleted
Obsoletes:	suspend < 1.0-10
Provides:	suspend = 1.0-10
Obsoletes:	suspend-s2ram < 1.0-10
Provides:	suspend-s2ram = 1.0-10
%endif
Provides:	should-restart = system
# (tpg) just to be sure we install this libraries
Requires:	libsystemd = %{EVRD}
Requires:	libsystemd-daemon = %{EVRD}
Requires:	libsystemd-login = %{EVRD}
Requires:	libsystemd-journal = %{EVRD}
Requires:	libsystemd-id128 = %{EVRD}
Requires:	nss_myhostname = %{EVRD}
#(tpg)for future releases... systemd provides also a full functional syslog tool
Provides:	syslog-daemon
# (tpg) conflict with old sysvinit subpackage
%rename		systemd-sysvinit
Conflicts:	systemd-sysvinit < 207-1
# (eugeni) systemd should work as a drop-in replacement for sysvinit, but not obsolete it
#SysVinit < %sysvinit_release-%sysvinit_release It's provides something
#like that SysVinit < 14-14 when it should be SysVinit 2.87-14
Provides:	sysvinit = %sysvinit_version-%sysvinit_release, SysVinit = %sysvinit_version-%sysvinit_release
# (tpg) time to die
Obsoletes:	sysvinit < %sysvinit_version-%sysvinit_release, SysVinit < %sysvinit_version-%sysvinit_release
# Due to halt/poweroff etc. in _bindir
Conflicts:	usermode-consoleonly < 1:1.110
Obsoletes:	hal <= 0.5.14-6
# (tpg) moved form makedev package
Provides:	dev
Obsoletes:	MAKEDEV < 4.4-23
Provides:	MAKEDEV = 4.4-23
Conflicts:	makedev < 4.4-23
Obsoletes:	readahead < 1.5.7-8
Provides:	readahead = 1.5.7-8
Obsoletes:	resolvconf < 1.75-3
Provides:	resolvconf = 1.75-3
Obsoletes:	bootchart < 2.0.11.4-3
Provides:	bootchart = 2.0.11.4-3
%rename		systemd-tools
%rename		systemd-units
%rename		udev

%description
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%if %{with uclibc}
%package -n uclibc-%{name}
Summary:	A System and Session Manager (uClibc linked)
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{EVRD}
Requires:	uclibc-%{libdaemon} = %{EVRD}
Requires:	uclibc-%{liblogin} = %{EVRD}
Requires:	uclibc-%{liblogin} = %{EVRD}
Requires:	uclibc-%{liblogin} = %{EVRD}
%rename		uclibc-udev

%description -n	uclibc-%{name}
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.
%endif

%package journal-gateway
Summary:	Gateway for serving journal events over the network using HTTP
Requires:	%{name} = %{EVRD}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Obsoletes:		systemd < 206-7

%description journal-gateway
Offers journal events over the network using HTTP.

%if !%{with bootstrap}
%package -n python-%{name}
Summary:	Python bindings for %{name}
Group:		Development/Python

%description -n python-%{name}
Python bindings for %{name}.
%endif

%package -n %{libsystemd}
Summary:	Systemdlibrary package
Group:		System/Libraries
Provides:	libsystemd = %{EVRD}

%description -n	%{libsystemd}
This package provides the systemd shared library.

%if %{with uclibc}
%package -n	uclibc-%{libsystemd}
Summary:	Systemd library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libsystemd}
This package provides the systemd shared library.

%package -n uclibc-%{libsystemd_devel}
Summary:	Systemd library development files
Group:		Development/C
Requires:	uclibc-%{libsystemd} = %{EVRD}
Requires:	%{libsystemd_devel} = %{EVRD}
Provides:	uclibc-libsystemd-devel = %{EVRD}
Conflicts:	%{libsystemd_devel} < 221-3

%description -n	uclibc-%{libsystemd_devel}
Development files for the systemd shared library.
%endif

%package -n %{libsystemd_devel}
Summary:	Systemd library development files
Group:		Development/C
Requires:	%{libsystemd} = %{EVRD}
Provides:	libsystemd-devel = %{EVRD}

%description -n	%{libsystemd_devel}
Development files for the systemd shared library.

%package -n %{libdaemon}
Summary:	Systemd-daemon library package
Group:		System/Libraries
Provides:	libsystemd-daemon = %{EVRD}

%description -n	%{libdaemon}
This package provides the systemd-daemon shared library.

%if %{with uclibc}
%package -n	uclibc-%{libdaemon}
Summary:	Systemd-daemon library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libdaemon}
This package provides the systemd-daemon shared library.

%package -n uclibc-%{libdaemon_devel}
Summary:	Systemd-daemon library development files
Group:		Development/C
Requires:	uclibc-%{libdaemon} = %{EVRD}
Requires:	%{libdaemon_devel} = %{EVRD}
Provides:	uclibc-libsystemd-daemon-devel = %{EVRD}
Conflicts:	%{libdaemon_devel} < 221-3

%description -n	uclibc-%{libdaemon_devel}
Development files for the systemd-daemon shared library.
%endif

%package -n %{libdaemon_devel}
Summary:	Systemd-daemon library development files
Group:		Development/C
Requires:	%{libdaemon} = %{EVRD}
Requires:	%{libsystemd_devel} = %{EVRD}
Provides:	libsystemd-daemon-devel = %{EVRD}
%rename		%{_lib}systemd-daemon0-devel

%description -n	%{libdaemon_devel}
Development files for the systemd-daemon shared library.

%package -n %{liblogin}
Summary:	Systemd-login library package
Group:		System/Libraries
Provides:	libsystemd-login = %{EVRD}

%description -n	%{liblogin}
This package provides the systemd-login shared library.

%if %{with uclibc}
%package -n uclibc-%{liblogin}
Summary:	Systemd-login library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{liblogin}
This package provides the systemd-login shared library.

%package -n uclibc-%{liblogin_devel}
Summary:	Systemd-login library development files
Group:		Development/C
Requires:	uclibc-%{liblogin} = %{EVRD}
Requires:	%{liblogin_devel} = %{EVRD}
Provides:	uclibc-libsystemd-login-devel = %{EVRD}
Conflicts:	%{liblogin_devel} < 221-3

%description -n	uclibc-%{liblogin_devel}
Development files for the systemd-login shared library.
%endif

%package -n %{liblogin_devel}
Summary:	Systemd-login library development files
Group:		Development/C
Requires:	%{liblogin} = %{EVRD}
Provides:	libsystemd-login-devel = %{EVRD}
%rename		%{_lib}systemd-login0-devel

%description -n	%{liblogin_devel}
Development files for the systemd-login shared library.

%package -n %{libjournal}
Summary:	Systemd-journal library package
Group:		System/Libraries
Provides:	libsystemd-journal = %{EVRD}

%description -n	%{libjournal}
This package provides the systemd-journal shared library.

%if %{with uclibc}
%package -n uclibc-%{libjournal}
Summary:	Systemd-journal library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libjournal}
This package provides the systemd-journal shared library.

%package -n uclibc-%{libjournal_devel}
Summary:	Systemd-journal library development files
Group:		Development/C
Requires:	uclibc-%{libjournal} = %{EVRD}
Requires:	%{libjournal_devel} = %{EVRD}
Provides:	uclibc-libsystemd-journal-devel = %{EVRD}
Requires:	%{libid128_devel} = %{EVRD}
Conflicts:	%{libjournal_devel} < 221-3

%description -n	uclibc-%{libjournal_devel}
Development files for the systemd-journal shared library.
%endif

%package -n %{libjournal_devel}
Summary:	Systemd-journal library development files
Group:		Development/C
Requires:	%{libjournal} = %{EVRD}
Provides:	libsystemd-journal-devel = %{EVRD}
%rename		%{_lib}systemd-journal0-devel
# sd-journal.h #includes sd-id128.h
Requires:	%{libid128_devel} = %{EVRD}

%description -n	%{libjournal_devel}
Development files for the systemd-journal shared library.

%package -n %{libid128}
Summary:	Systemd-id128 library package
Group:		System/Libraries
Provides:	libsystemd-id128 = %{EVRD}
# (tpg) cooker only, should be removed soon
%rename		%{_lib}systemd-id1280

%description -n	%{libid128}
This package provides the systemd-id128 shared library.

%if %{with uclibc}
%package -n uclibc-%{libid128}
Summary:	Systemd-id128 library package (uClibc linked)
Group:		System/Libraries
%rename		uclibc-%{_lib}systemd-id1280

%description -n	uclibc-%{libid128}
This package provides the systemd-id128 shared library.

%package -n uclibc-%{libid128_devel}
Summary:	Systemd-id128 library development files
Group:		Development/C
Requires:	uclibc-%{libid128} = %{EVRD}
Requires:	%{libid128_devel} = %{EVRD}
Provides:	uclibc-libsystemd-id128-devel = %{EVRD}
Conflicts:	%{libid128_devel} < 221-3

%description -n uclibc-%{libid128_devel}
Development files for the systemd-id128 shared library.
%endif

%package -n %{libid128_devel}
Summary:	Systemd-id128 library development files
Group:		Development/C
Requires:	%{libid128} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libid128} = %{EVRD}
%endif
Provides:	libsystemd-id128-devel = %{EVRD}
%rename		%{_lib}systemd-id1280-devel

%description -n %{libid128_devel}
Development files for the systemd-id128 shared library.

%package -n %{libnss_myhostname}
Summary:	Library for local system host name resolution
Group:		System/Libraries
Provides:	libnss_myhostname = %{EVRD}
Provides:	nss_myhostname = %{EVRD}
Obsoletes:	nss_myhostname <= 0.3-1
Requires(post,preun):	bash
Requires(post,preun):	sed
Requires(post,preun):	glibc

%description -n %{libnss_myhostname}
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%if %{with uclibc}
%package -n uclibc-%{libnss_myhostname}
Summary:	Library for local system host name resolution (uClibc linked)
Group:		System/Libraries

%description -n uclibc-%{libnss_myhostname}
uClibc version of nss-myhostname.
%endif

%package -n %{libudev}
Summary:	Library for udev
Group:		System/Libraries
Obsoletes:	%{mklibname hal 1} <= 0.5.14-6

%description -n	%{libudev}
Library for udev.

%if %{with uclibc}
%package -n uclibc-%{libudev}
Summary:	Library for udev (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libudev}
Library for udev.

%package -n uclibc-%{libudev_devel}
Summary:	Devel library for udev
Group:		Development/C
License:	LGPLv2+
Provides:	uclibc-udev-devel = %{EVRD}
Requires:	uclibc-%{libudev} = %{EVRD}
Requires:	%{libudev_devel} = %{EVRD}
Conflicts:	%{libudev_devel} < 221-3

%description -n	uclibc-%{libudev_devel}
Devel library for udev.
%endif

%package -n %{libudev_devel}
Summary:	Devel library for udev
Group:		Development/C
License:	LGPLv2+
Provides:	udev-devel = %{EVRD}
Requires:	%{libudev} = %{EVRD}
Obsoletes:	%{_lib}udev0-devel
Obsoletes:	%{name}-doc

%description -n	%{libudev_devel}
Devel library for udev.

%package -n udev-doc
Summary:	Udev documentation
Group:		Books/Computer books

%description -n	udev-doc
This package contains documentation of udev.

%prep
%setup -q
%apply_patches

find src/ -name "*.vala" -exec touch '{}' \;
find -type d |xargs chmod 755

# (tpg) handle -Oz to enable -flto
sed -i -e "/^AS_CASE/s/12345/12345z/" configure*

#intltoolize --force --automake
autoreconf -fiv

%build
export CONFIGURE_TOP="$PWD"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--prefix=%{_prefix} \
	--with-rootprefix="" \
	--with-rootlibdir=%{uclibc_root}/%{_lib} \
	--libexecdir=%{_prefix}/lib \
	--enable-compat-libs \
	--enable-static \
	--enable-chkconfig \
	--with-sysvinit-path=%{_initrddir} \
	--with-sysvrcnd-path=%{_sysconfdir}/rc.d \
	--with-rc-local-script-path-start=/etc/rc.d/rc.local \
	--disable-selinux \
	--disable-seccomp \
	--enable-split-usr \
	--enable-introspection=no \
	--disable-gudev \
	--disable-qrencode \
	--disable-microhttpd \
	--disable-pam \
%if %{with bootstrap}
	--disable-libcryptsetup \
%else
	--enable-libcryptsetup	\
%endif
	--enable-gcrypt \
	--disable-audit \
	--disable-manpages \
	--without-python \
	--disable-selinux \
	--disable-libidn \
	--disable-gnutls \
	--disable-elfutils \
	--disable-libcurl \
	--disable-sysusers \
	--disable-resolved \
	--disable-networkd \
	--disable-localed \
	--disable-coredump \
	--disable-timesyncd \
	--disable-timedated \
	--disable-hostnamed \
	--disable-machined \
	--disable-bootchart \
	--disable-quotacheck \
	--disable-libiptc \
	--disable-gnuefi \
	--with-kbd-loadkeys=/bin/loadkeys \
	--with-kbd-setfont=/bin/setfont \
	--disable-kdbus \
	--with-ntp-servers="0.openmandriva.pool.ntp.org 1.openmandriva.pool.ntp.org 2.openmandriva.pool.ntp.org 3.openmandriva.pool.ntp.org" \
	--with-dns-servers="208.67.222.222 208.67.220.220"

%make

popd
%endif

# This has to go after the uClibc build -- uClibc doesn't have
# functions needed for SSP
%serverbuild_hardened
mkdir -p shared
pushd shared
%configure \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib} \
	--libexecdir=%{_prefix}/lib \
	--enable-compat-libs \
	--enable-bzip2 \
	--enable-lz4 \
	--disable-static \
	--enable-chkconfig \
	--with-sysvinit-path=%{_initrddir} \
	--with-sysvrcnd-path=%{_sysconfdir}/rc.d \
	--with-rc-local-script-path-start=/etc/rc.d/rc.local \
	--disable-selinux \
	--disable-gudev \
%ifnarch %armx
	--enable-gnuefi \
%endif
%if %{with bootstrap}
	--enable-introspection=no \
	--disable-libcryptsetup \
	--without-python \
%else
	--enable-introspection=no \
%endif
	--enable-split-usr \
	--enable-xkbcommon \
	--with-kbd-loadkeys=/bin/loadkeys \
	--with-kbd-setfont=/bin/setfont \
	--disable-kdbus \
	--with-ntp-servers="0.openmandriva.pool.ntp.org 1.openmandriva.pool.ntp.org 2.openmandriva.pool.ntp.org 3.openmandriva.pool.ntp.org" \
	--with-dns-servers="208.67.222.222 208.67.220.220"

%make

popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
mv %{buildroot}/bin %{buildroot}%{uclibc_root}/bin
mkdir -p %{buildroot}%{uclibc_root}/sbin
ln -sf %{uclibc_root}/bin/udevadm %{buildroot}%{uclibc_root}/sbin
rm -f %{buildroot}%{uclibc_root}%{_bindir}/systemd-analyze
rm -rf %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{uclibc_root}%{python_sitelib}/%{name}
%endif

%makeinstall_std -C shared

mkdir -p %{buildroot}{/bin,%{_sbindir}}

# (bor) create late shutdown and sleep directory
mkdir -p %{buildroot}%{systemd_libdir}/system-shutdown
mkdir -p %{buildroot}%{systemd_libdir}/system-sleep

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/sbin
ln -s ..%{systemd_libdir}/systemd %{buildroot}/sbin/init
ln -s ..%{systemd_libdir}/systemd %{buildroot}/bin/systemd

# (tpg) install compat symlinks
for i in halt poweroff reboot; do
	ln -s /bin/systemctl %{buildroot}/bin/$i
done

for i in runlevel shutdown telinit; do
	ln -s ../bin/systemctl %{buildroot}/sbin/$i
done

ln -s /bin/loginctl %{buildroot}%{_bindir}/systemd-loginctl
%if %{with uclibc}
ln -srf %{buildroot}%{uclibc_root}/bin/loginctl %{buildroot}%{uclibc_root}%{_bindir}/systemd-loginctl
%endif

# (tpg) dracut needs this
ln -s /bin/systemctl %{buildroot}%{_bindir}/systemctl

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/systemd/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}/%{systemd_libdir}/system/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/dbus.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/syslog.target.wants
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/getty.target.wants

#(tpg) keep these compat symlink
ln -s -r %{buildroot}/%{systemd_libdir}/system/systemd-udevd.service %{buildroot}/%{systemd_libdir}/system/udev.service
ln -s -r %{buildroot}/%{systemd_libdir}/system/systemd-udev-settle.service %{buildroot}/%{systemd_libdir}/system/udev-settle.service


# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/systemd/system/default.target

# (tpg) this is needed
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-generators
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-generators

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}/%{systemd_libdir}/system/bluetooth.target.wants

# (tpg) use systemd's own mounting capability
sed -i -e 's/^#MountAuto=yes$/MountAuto=yes/' %{buildroot}/etc/systemd/system.conf
sed -i -e 's/^#SwapAuto=yes$/SwapAuto=yes/' %{buildroot}/etc/systemd/system.conf

# (bor) enable rpcbind.target by default so we have something to plug portmapper service into
ln -s ../rpcbind.target %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants

# (tpg) explicitly enable these services
ln -sf /lib/systemd/system/systemd-resolved.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/systemd-resolved.service
ln -sf /lib/systemd/system/systemd-networkd.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/systemd-networkd.service
ln -sf /lib/systemd/system/systemd-timesyncd.service %{buildroot}/%{systemd_libdir}/system/sysinit.target.wants/systemd-timesyncd.service

# (eugeni) install /run
mkdir %{buildroot}/run

# (tpg) create missing dir
mkdir -p %{buildroot}%{_libdir}/systemd/user/
mkdir -p %{buildroot}%{_sysconfdir}/systemd/user/default.target.wants

# Create new-style configuration files so that we can ghost-own them
touch %{buildroot}%{_sysconfdir}/hostname
touch %{buildroot}%{_sysconfdir}/vconsole.conf
touch %{buildroot}%{_sysconfdir}/locale.conf
touch %{buildroot}%{_sysconfdir}/machine-id
touch %{buildroot}%{_sysconfdir}/machine-info
touch %{buildroot}%{_sysconfdir}/timezone
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d
touch %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
mkdir -p %{buildroot}%{_sysconfdir}/udev
touch %{buildroot}%{_sysconfdir}/udev/hwdb.bin

# (cg) Set up the pager to make it generally more useful
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh << EOF
export SYSTEMD_PAGER="/usr/bin/less -FR"
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh

# (tpg) move to etc
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
mv -f %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.systemd %{buildroot}%{_sysconfdir}/rpm/macros.d/systemd.macros

# Install logdir for journald
install -m 0755 -d %{buildroot}%{_logdir}/journal

# (tpg) Install default distribution preset policy for services
mkdir -p %{buildroot}%{systemd_libdir}/system-preset/
mkdir -p %{buildroot}%{systemd_libdir}/user-preset/

# (tpg) install presets
install -m 0644 %{SOURCE12} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE13} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE14} %{buildroot}%{systemd_libdir}/system-preset/

# (tpg) install network file
install -m 0644 %{SOURCE17} %{buildroot}%{systemd_libdir}/network/
# (fedya) install wireless file
install -m 0644 %{SOURCE20} %{buildroot}%{systemd_libdir}/network/

# (tpg) install userspace presets
install -m 0644 %{SOURCE18} %{buildroot}%{systemd_libdir}/user-preset/

# Install rsyslog fragment
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/rsyslog.d/

# (tpg) silent kernel messages
# print only KERN_ERR and more serious alerts
echo "kernel.printk = 3 3 3 3" >> %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) by default enable SysRq
sed -i -e 's/^#kernel.sysrq = 0/kernel.sysrq = 1/' %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) use 100M as a default maximum value for journal logs
sed -i -e 's/^#SystemMaxUse=.*/SystemMaxUse=100M/' %{buildroot}%{_sysconfdir}/systemd/journald.conf

#################
#	UDEV	#
#	START	#
#################

install -m 644 %{SOURCE2} %{buildroot}%{udev_rules_dir}/
install -m 644 %{SOURCE3} %{buildroot}%{udev_rules_dir}/
mkdir -p  %{buildroot}%{_sysconfdir}/sysconfig/udev
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/udev/

# net rules
install -m 0644 %{SOURCE6} %{buildroot}%{udev_rules_dir}/
install -m 0755 %{SOURCE7} %{buildroot}%{udev_libdir}/net_create_ifcfg
install -m 0755 %{SOURCE8} %{buildroot}%{udev_libdir}/net_action
install -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/udev_net

install -m 0644 %{SOURCE10} %{buildroot}%{udev_rules_dir}/
install -m 0644 %{SOURCE19} %{buildroot}%{udev_rules_dir}/

# probably not required, but let's just be on the safe side for now..
ln -sf /bin/udevadm %{buildroot}/sbin/udevadm
ln -sf /bin/udevadm %{buildroot}%{_bindir}/udevadm
ln -sf /bin/udevadm %{buildroot}%{_sbindir}/udevadm

# (tpg) this is needed, because udevadm is in /bin
# altering the path allows to boot on before root pivot
sed -i --follow-symlinks -e 's#/bin/udevadm#/sbin/udevadm#g' %{buildroot}/%{systemd_libdir}/system/*.service

mkdir -p %{buildroot}%{_prefix}/lib/firmware/updates
mkdir -p %{buildroot}%{_sysconfdir}/udev/agents.d/usb
touch %{buildroot}%{_sysconfdir}/scsi_id.config

ln -s ..%{systemd_libdir}/systemd-udevd %{buildroot}/sbin/udevd
ln -s %{systemd_libdir}/systemd-udevd %{buildroot}%{udev_libdir}/udevd

# udev rules for zte 3g modems and drakx-net

mkdir -p %{buildroot}/lib/firmware/updates
# default /dev content, from Fedora RPM
mkdir -p %{buildroot}%{udev_libdir}/devices/{net,hugepages,pts,shm}
# From previous Mandriva /etc/udev/devices.d
mkdir -p %{buildroot}%{udev_libdir}/devices/cpu/0

#################
#	UDEV	#
#	END	#
#################

# (tpg) just delete this for now
# file /usr/share/man/man5/crypttab.5.xz 
# from install of systemd-186-2.x86_64
# conflicts with file from package initscripts-9.25-10.x86_64
rm -rf %{buildroot}%{_mandir}/man5/crypttab*

%find_lang %{name}

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 -o $2 -ge 2 ] ; then
	/bin/systemctl daemon-reexec 2>&1 || :
fi

%pre
if [ $1 -ge 2 ]; then
# (tpg) add input group
if ! getent group input >/dev/null 2>&1; then
	/usr/sbin/groupadd -r input >/dev/null || :
fi

# (cg) Cannot use rpm-helper scripts as it results in a cyclical dep as
# rpm-helper requires systemd-units which in turn requires systemd...
if ! getent group %{name}-journal >/dev/null 2>&1; then
	/usr/sbin/groupadd -r %{name}-journal >/dev/null || :
fi

# (tpg) add timesync group and user
if ! getent group %{name}-timesync >/dev/null 2>&1; then
	/usr/sbin/groupadd -r %{name}-timesync >/dev/null || :
fi

if ! getent passwd %{name}-timesync >/dev/null 2>&1; then
	/usr/sbin/useradd -r -l -g systemd-timesync -d / -s /sbin/nologin -c "systemd timesync" systemd-timesync >/dev/null 2>&1 || :
fi

# (tpg) add network group and user
if ! getent group %{name}-network >/dev/null 2>&1; then
	/usr/sbin/groupadd -r %{name}-network >/dev/null || :
fi

if ! getent passwd %{name}-network >/dev/null 2>&1; then
	/usr/sbin/useradd -r -l -g systemd-network -d / -s /sbin/nologin -c "systemd network" systemd-network >/dev/null 2>&1 || :
fi

# (tpg) add resolve group and user
if ! getent group %{name}-resolve >/dev/null 2>&1; then
	/usr/sbin/groupadd -r %{name}-resolve >/dev/null || :
fi

if ! getent passwd %{name}-resolve >/dev/null 2>&1; then
	/usr/sbin/useradd -r -l -g systemd-resolve -d / -s /sbin/nologin -c "systemd resolver" systemd-resolve >/dev/null 2>&1 || :
fi

# (tpg) add busproxy group and user
if ! getent group %{name}-bus-proxy >/dev/null 2>&1; then
	/usr/sbin/groupadd -r %{name}-bus-proxy >/dev/null || :
fi

if ! getent passwd %{name}-busproxy >/dev/null 2>&1; then
	/usr/sbin/useradd -r -l -g systemd-bus-proxy -d / -s /sbin/nologin -c "systemd proxy" systemd-bus-proxy >/dev/null 2>&1 || :
fi


systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :
fi

%post
/bin/systemd-machine-id-setup >/dev/null 2>&1 ||:
%{systemd_libdir}/systemd-random-seed save >/dev/null 2>&1 || :
/bin/systemctl daemon-reexec >/dev/null 2>&1 || :
/bin/systemctl start systemd-udevd.service >/dev/null 2>&1 || :
/bin/systemd-hwdb update >/dev/null 2>&1 || :
/bin/journalctl --update-catalog >/dev/null 2>&1 || :

# (tpg) do not use fistboot here as id hangs on firstboot in lxc :)
# systemd-firstboot --setup-machine-id
systemd-sysusers

%if %mdvver < 201500
if [ $1 -ge 2 ]; then
#(tpg) BIG migration
# Migrate /etc/sysconfig/clock
  if [ ! -L /etc/localtime -a -e /etc/sysconfig/clock ] ; then
	  . /etc/sysconfig/clock 2>&1 || :
	  if [ -n "$ZONE" -a -e "/usr/share/zoneinfo/$ZONE" ] ; then
	      /usr/bin/ln -sf "../usr/share/zoneinfo/$ZONE" /etc/localtime >/dev/null 2>&1 || :
	  fi
  fi

# Migrate /etc/sysconfig/i18n
  if [ -e /etc/sysconfig/i18n -a ! -e /etc/locale.conf ]; then
	  unset LANGUAGE
	  unset LANG
	  unset LC_CTYPE
	  unset LC_NUMERIC
	  unset LC_TIME
	  unset LC_COLLATE
	  unset LC_MONETARY
	  unset LC_MESSAGES
	  unset LC_PAPER
	  unset LC_NAME
	  unset LC_ADDRESS
	  unset LC_TELEPHONE
	  unset LC_MEASUREMENT
	  unset LC_IDENTIFICATION
	  . /etc/sysconfig/i18n >/dev/null 2>&1 || :
	  [ -n "$LANGUAGE" ] && echo LANG=$LANGUAGE > /etc/locale.conf 2>&1 || :
	  [ -n "$LANG" ] && echo LANG=$LANG >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_CTYPE" ] && echo LC_CTYPE=$LC_CTYPE >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_NUMERIC" ] && echo LC_NUMERIC=$LC_NUMERIC >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_TIME" ] && echo LC_TIME=$LC_TIME >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_COLLATE" ] && echo LC_COLLATE=$LC_COLLATE >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_MONETARY" ] && echo LC_MONETARY=$LC_MONETARY >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_MESSAGES" ] && echo LC_MESSAGES=$LC_MESSAGES >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_PAPER" ] && echo LC_PAPER=$LC_PAPER >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_NAME" ] && echo LC_NAME=$LC_NAME >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_ADDRESS" ] && echo LC_ADDRESS=$LC_ADDRESS >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_TELEPHONE" ] && echo LC_TELEPHONE=$LC_TELEPHONE >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_MEASUREMENT" ] && echo LC_MEASUREMENT=$LC_MEASUREMENT >> /etc/locale.conf 2>&1 || :
	  [ -n "$LC_IDENTIFICATION" ] && echo LC_IDENTIFICATION=$LC_IDENTIFICATION >> /etc/locale.conf 2>&1 || :
  fi

# Migrate /etc/sysconfig/keyboard to the vconsole configuration
  if [ -e /etc/sysconfig/keyboard -a ! -e /etc/vconsole.conf ]; then
	  unset SYSFONT
	  unset SYSFONTACM
	  unset UNIMAP
	  unset KEYMAP
	  [ -e /etc/sysconfig/i18n ] && . /etc/sysconfig/i18n >/dev/null 2>&1 || :
	  . /etc/sysconfig/keyboard >/dev/null 2>&1 || :
	  [ -n "$SYSFONT" ] && echo FONT=$SYSFONT > /etc/vconsole.conf 2>&1 || :
	  [ -n "$SYSFONTACM" ] && echo FONT_MAP=$SYSFONTACM >> /etc/vconsole.conf 2>&1 || :
	  [ -n "$UNIMAP" ] && echo FONT_UNIMAP=$UNIMAP >> /etc/vconsole.conf 2>&1 || :
	  [ -n "$KEYTABLE" ] && echo KEYMAP=$KEYTABLE >> /etc/vconsole.conf 2>&1 || :
  fi

# Migrate /etc/sysconfig/keyboard to the X11 keyboard configuration
  if [ -e /etc/sysconfig/keyboard -a ! -e %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf ]; then
	  unset XkbLayout
	  unset XkbModel
	  unset XkbVariant
	  unset XkbOptions
	  . /etc/sysconfig/keyboard >/dev/null 2>&1 || :

	  echo "Section \"InputClass\"" > %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  echo "        Identifier \"system-keyboard\"" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  echo "        MatchIsKeyboard \"on\"" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  [ -n "$XkbLayout" ]  && echo "        Option \"XkbLayout\" \"$XkbLayout\"" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  [ -n "$XkbModel" ]   && echo "        Option \"XkbModel\" \"$XkbModel\"" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  [ -n "$XkbVariant" ] && echo "        Option \"XkbVariant\" \"$XkbVariant\"" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  [ -n "$XkbOptions" ] && echo "        Option \"XkbOptions\" \"$XkbOptions\"" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
	  echo "EndSection" >> %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf 2>/dev/null || :
  fi

  rm -f /etc/sysconfig/i18n >/dev/null 2>&1 || :
  rm -f /etc/sysconfig/keyboard >/dev/null 2>&1 || :

# Migrate HOSTNAME= from /etc/sysconfig/network
  if [ -e /etc/sysconfig/network -a ! -e /etc/hostname ]; then
	  unset HOSTNAME
	  . /etc/sysconfig/network >/dev/null 2>&1 || :
	  [ -n "$HOSTNAME" ] && echo $HOSTNAME > /etc/hostname 2>&1 || :
  fi

  /usr/bin/sed -i '/^HOSTNAME=/d' /etc/sysconfig/network >/dev/null 2>&1 || :
fi
%endif
# End BIG migration

# (tpg) move sysctl.conf to /etc/sysctl.d as since 207 /etc/sysctl.conf is skipped
if [ $1 -ge 2 ]; then
    if [ -e %{_sysconfdir}/sysctl.conf ] && [ ! -L %{_sysconfdir}/sysctl.conf ]; then
	mv -f %{_sysconfdir}/sysctl.conf %{_sysconfdir}/sysctl.d/99-sysctl.conf
	ln -s %{_sysconfdir}/sysctl.d/99-sysctl.conf %{_sysconfdir}/sysctl.conf
    fi
fi

# (tpg) from old units package
if [ $1 -eq 2 ] ; then
        # Try to read default runlevel from the old inittab if it exists
        runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
        if [ -z "$runlevel" ] ; then
                target="/lib/systemd/system/graphical.target"
        else
                target="/lib/systemd/system/runlevel$runlevel.target"
        fi

        # And symlink what we found to the new-style default.target
        /bin/ln -sf "$target" %{_sysconfdir}/systemd/system/default.target 2>&1 || :
	# (tpg) need to restart it to catch new auth
	/bin/systemctl try-restart systemd-logind.service 2>&1 || :
fi

# Enable the services we install by default.
/bin/systemctl --quiet preset \
       getty@tty1.service \
       remote-fs.target \
       shadow.timer \
       shadow.service \
       systemd-firstboot.service \
       systemd-networkd.service \
       systemd-resolved.service \
       systemd-timesyncd.service \
       systemd-timedated.service \
       systemd-udev-settle.service \
        2>&1 || :

hostname_new=`cat %{_sysconfdir}/hostname 2>/dev/null`
if [ -z $hostname_new ]; then
        hostname_old=`cat /etc/sysconfig/network 2>/dev/null | grep HOSTNAME | cut -d "=" -f2`
	if [ ! -z $hostname_old ]; then
    		echo $hostname_old >> %{_sysconfdir}/hostname
        else
    		echo "localhost" >> %{_sysconfdir}/hostname
        fi
fi

%preun
if [ $1 -eq 0 ] ; then
    /bin/systemctl --quiet disable \
           getty@tty1.service \
           getty@getty.service \
           remote-fs.target \
           systemd-networkd.service \
           systemd-resolvd.service \
           systemd-timesync.service \
           systemd-timedated.service \
           console-getty.service \
           console-shell.service \
           debug-shell.service \
           2>&1 || :

    /bin/rm -f /etc/systemd/system/default.target 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
  systemctl daemon-reload > /dev/null 2>&1 || :
fi

%posttrans
# (tpg) handle resolvconf
if [ -f /etc/resolv.conf ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ ! -e /etc/resolv.conf ]; then
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" = "/run/resolvconf/resolv.conf" ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" = "/run/NetworkManager/resolv.conf" ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
fi

# workarounds for ABF
if [ ! -f /run/systemd/resolve/resolv.conf ]; then
    echo "Warning /run/systemd/resolve/resolv.conf does not exists. Recreating it."
    mkdir -p /run/systemd/resolve
    echo -e "nameserver 208.67.222.222\nnameserver 208.67.220.220\n" > /run/systemd/resolve/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
fi
# end of workarounds

%triggerin -- setup
# setup package owns /etc/resolv.conf
# so on every setup update /etc/resolv.conf needs to be symlinked
# to /run/systemd/resolve/resolv.conf
if [ $1 -ge 2 -o $2 -ge 2 ]; then
    if [ -f /etc/resolv.conf ]; then
		rm -f /etc/resolv.conf
		ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
    fi
    /bin/systemctl enable systemd-resolved.service 2>&1 || :
    /bin/systemctl restart systemd-resolved.service 2>&1 || :
fi

%triggerun -- %{name} < 196
%{_bindir}/systemctl restart systemd-logind.service

%triggerun -- %{name} < 208-2
chgrp -R systemd-journal /var/log/journal || :
chmod 02755 /var/log/journal || :
if [ -f /etc/machine-id ]; then
	chmod 02755 /var/log/journal/$(cat /etc/machine-id) || :
fi

%triggerposttransun -- resolvconf < 1.75-4
if [ -f /etc/resolv.conf ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ ! -e /etc/resolv.conf ]; then
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" = "/run/resolvconf/resolv.conf" ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
elif [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" = "/run/NetworkManager/resolv.conf" ]; then
    rm -f /etc/resolv.conf
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
fi

/bin/systemctl enable systemd-resolved.service 2>&1 || :
/bin/systemctl restart systemd-resolved.service 2>&1 || :

%triggerposttransin -- %{_tmpfilesdir}/*.conf
if [ $1 -eq 1 -o $2 -eq 1 ]; then
    while [ -n "$3" ]; do
        if [ -f "$3" ]; then
            /bin/systemd-tmpfiles --create "$3"
        fi
        shift
    done
fi

%triggerposttransun -- %{_tmpfilesdir}/*.conf
if [ $2 -eq 0 ]; then
    while [ -n "$3" ]; do
        if [ -f "$3" ]; then
            /bin/systemd-tmpfiles --remove "$3"
        fi
        shift
    done
fi

%triggerin -- %{name}-units < 217-10
# make sure we use preset here
/bin/systemctl --quiet preset \
	getty@getty.service \
	remote-fs.target \
	systemd-readahead-replay.service \
	systemd-readahead-collect.service \
	console-getty.service \
	console-shell.service \
	debug-shell.service \
	2>&1 || :

/bin/systemctl --quiet stop getty@getty.service 2>&1 || :
/bin/systemctl --quiet disable getty@getty.service 2>&1 || :
/bin/systemctl --quiet stop systemd-readahead-replay.service 2>&1 || :
/bin/systemctl --quiet stop systemd-readahead-collect.service 2>&1 || :
/bin/systemctl --quiet disable systemd-readahead-replay.service 2>&1 || :
/bin/systemctl --quiet disable systemd-readahead-collect.service 2>&1 || :

%triggerpostun -- %{name}-units < 217-10
# remove wrong getty target
if [ -d %{_sysconfdir}/systemd/system/getty.target.wants/getty@getty.service ]
	/bin/systemctl --quiet disable getty@getty.service  2>&1 || :
    rm -rf %{_sysconfdir}/systemd/system/getty.target.wants ||:
fi

%triggerin -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
ARG1=$1
ARG2=$2
shift
shift

units=${*#%{_unitdir}/}
if [ $ARG1 -eq 1 -a $ARG2 -eq 1 ]; then
    /bin/systemctl preset ${units} >/dev/null 2>&1 || :
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%triggerun -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
ARG1=$1
ARG2=$2
shift
shift

skip="$(grep -l 'Alias=display-manager.service' $*)"
units=${*#%{_unitdir}/}
units=${units#${skip##*/}}
if [ $ARG2 -eq 0 ]; then
    /bin/systemctl --no-reload disable ${units} >/dev/null 2>&1 || :
    /bin/systemctl stop ${units} >/dev/null 2>&1 || :
fi

%triggerpostun -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%triggerposttransin -- %{_binfmtdir}/*.conf
systemctl reload-or-try-restart systemd-binfmt

%triggerposttransun -- %{_binfmtdir}/*.conf
systemctl reload-or-try-restart systemd-binfmt

%post -n %{libnss_myhostname}
# sed-fu to add myhostname to the hosts line of /etc/nsswitch.conf
if [ -f /etc/nsswitch.conf ] ; then
	sed -i.bak -e '
	    /^hosts:/ !b
	    /\<myhostname\>/ b
	    s/[[:blank:]]*$/ myhostname/
	    ' /etc/nsswitch.conf
fi

%preun -n %{libnss_myhostname}
# sed-fu to remove myhostname from the hosts line of /etc/nsswitch.conf
if [ "$1" -eq 0 -a -f /etc/nsswitch.conf ] ; then
	sed -i.bak -e '
	    /^hosts:/ !b
	    s/[[:blank:]]\+myhostname\>//
	    ' /etc/nsswitch.conf
fi

%pre journal-gateway
%_pre_groupadd systemd-journal-gateway systemd-journal-gateway
%_pre_useradd systemd-journal-gateway %{_var}/log/journal /sbin/nologin
%_pre_groupadd systemd-journal-remote systemd-journal-remote
%_pre_useradd systemd-journal-remote %{_var}/log/journal/remote /sbin/nologin
%_pre_groupadd systemd-journal-upload systemd-journal-upload
%_pre_useradd systemd-journal-upload %{_var}/log/journal/upload /sbin/nologin

%files -f %{name}.lang
%doc %{_docdir}/systemd
%dir /lib/firmware
%dir /lib/firmware/updates
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%dir %{_datadir}/systemd
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/boot
%dir %{_prefix}/lib/systemd/boot/efi
%dir %{_prefix}/lib/systemd/catalog
%dir %{_prefix}/lib/systemd/system-generators
%dir %{_prefix}/lib/systemd/user
%dir %{_prefix}/lib/systemd/user-generators
%dir %{_prefix}/lib/sysusers.d
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/system/getty.target.wants
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/user/default.target.wants
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/agents.d
%dir %{_sysconfdir}/udev/agents.d/usb
%dir %{_sysconfdir}/udev/rules.d
%dir %{systemd_libdir}
%dir %{systemd_libdir}/*-generators
%dir %{systemd_libdir}/network
%dir %{systemd_libdir}/system
%dir %{systemd_libdir}/system-preset
%dir %{systemd_libdir}/system-shutdown
%dir %{systemd_libdir}/system-sleep
%dir %{systemd_libdir}/system/basic.target.wants
%dir %{systemd_libdir}/system/bluetooth.target.wants
%dir %{systemd_libdir}/system/busnames.target.wants
%dir %{systemd_libdir}/system/dbus.target.wants
%dir %{systemd_libdir}/system/default.target.wants
%dir %{systemd_libdir}/system/graphical.target.wants
%dir %{systemd_libdir}/system/local-fs.target.wants
%dir %{systemd_libdir}/system/multi-user.target.wants
%dir %{systemd_libdir}/system/rescue.target.wants
%dir %{systemd_libdir}/system/runlevel1.target.wants
%dir %{systemd_libdir}/system/runlevel2.target.wants
%dir %{systemd_libdir}/system/runlevel3.target.wants
%dir %{systemd_libdir}/system/runlevel4.target.wants
%dir %{systemd_libdir}/system/runlevel5.target.wants
%dir %{systemd_libdir}/system/sockets.target.wants
%dir %{systemd_libdir}/system/sysinit.target.wants
%dir %{systemd_libdir}/system/syslog.target.wants
%dir %{systemd_libdir}/system/timers.target.wants
%dir %{systemd_libdir}/user-preset
%dir %{udev_libdir}
%dir %{udev_libdir}/hwdb.d
%dir %{udev_rules_dir}
%exclude %{_mandir}/man8/libnss_myhostname.so.2.8.*
%exclude %{_mandir}/man8/libnss_mymachines.so.2.8.*
%exclude %{_mandir}/man8/nss-myhostname.8.*
%exclude %{_mandir}/man8/nss-mymachines.8.*
%exclude %{_mandir}/man8/systemd-journal-gatewayd.8.*
%exclude %{_mandir}/man8/systemd-journal-gatewayd.service.8.*
%exclude %{_mandir}/man8/systemd-journal-gatewayd.socket.8.*
%exclude %{_mandir}/man8/systemd-journal-remote.8.*
%exclude %{_mandir}/man8/systemd-journal-upload.8.*
%exclude %{_prefix}/lib/tmpfiles.d/systemd-remote.conf
%exclude %{systemd_libdir}/system/systemd-journal-gatewayd.service
%exclude %{systemd_libdir}/system/systemd-journal-gatewayd.socket
%exclude %{systemd_libdir}/system/systemd-journal-remote.service
%exclude %{systemd_libdir}/system/systemd-journal-remote.socket
%exclude %{systemd_libdir}/system/systemd-journal-upload.service
%exclude %{systemd_libdir}/systemd-journal-gatewayd
%exclude %{systemd_libdir}/systemd-journal-remote
%exclude %{systemd_libdir}/systemd-journal-upload
%exclude %config(noreplace) %{_prefix}/lib/sysusers.d/systemd-remote.conf
%exclude %config(noreplace) %{_sysconfdir}/systemd/journal-remote.conf
%exclude %config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%ghost %{_sysconfdir}/udev/hwdb.bin
%ghost %config(noreplace,missingok) %attr(0644,root,root) %{_sysconfdir}/scsi_id.config
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/*.conf
/%{_lib}/security/pam_systemd.so
/bin/halt
/bin/journalctl
/bin/loginctl
/bin/machinectl
/bin/networkctl
/bin/poweroff
/bin/reboot
/bin/systemctl
/bin/systemd
/bin/systemd-ask-password
/bin/systemd-escape
/bin/systemd-firstboot
/bin/systemd-hwdb
/bin/systemd-inhibit
/bin/systemd-machine-id-setup
/bin/systemd-notify
/bin/systemd-sysusers
/bin/systemd-tmpfiles
/bin/systemd-tty-ask-password-agent
/bin/udevadm
/sbin/init
/sbin/runlevel
/sbin/shutdown
/sbin/telinit
%{_bindir}/bootctl
%{_bindir}/busctl
%{_bindir}/coredumpctl
%{_bindir}/hostnamectl
%{_bindir}/kernel-install
%{_bindir}/localectl
%{_bindir}/systemctl
%{_bindir}/systemd-*
%{_bindir}/timedatectl
%{_datadir}/bash-completion/completions/*
%{_datadir}/dbus-1/*services/*.service
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/systemd/kbd-model-map
%{_datadir}/systemd/language-fallback-map
%{_datadir}/zsh/site-functions/*
%{_initrddir}/README
%{_logdir}/README
%{_mandir}/man1/*.*
%{_mandir}/man3/*.*
%{_mandir}/man5/*.*
%{_mandir}/man7/*.*
%{_mandir}/man8/*.*
%{_prefix}/lib/kernel/install.d/*.install
%ifnarch %armx
%{_prefix}/lib/systemd/boot/efi/*.efi
%{_prefix}/lib/systemd/boot/efi/*.stub
%endif
%{_prefix}/lib/systemd/catalog/*.catalog
%{_prefix}/lib/systemd/user-generators/systemd-dbus1-generator
%{_prefix}/lib/systemd/user/*.service
%{_prefix}/lib/systemd/user/*.socket
%{_prefix}/lib/systemd/user/*.target
%{_prefix}/lib/tmpfiles.d/*.conf
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/rpm/macros.d/systemd.macros
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/xdg/systemd
%{systemd_libdir}/*-generators/*
%{systemd_libdir}/import-pubring.gpg
%{systemd_libdir}/network/80-container-host0.network
%{systemd_libdir}/network/80-container-ve.network
%{systemd_libdir}/network/90-enable.network
%{systemd_libdir}/network/90-wireless.network
%{systemd_libdir}/network/99-default.link
%{systemd_libdir}/system-preset/*.preset
%{systemd_libdir}/system/*.automount
%{systemd_libdir}/system/*.busname
%{systemd_libdir}/system/*.mount
%{systemd_libdir}/system/*.path
%{systemd_libdir}/system/*.service
%{systemd_libdir}/system/*.slice
%{systemd_libdir}/system/*.socket
%{systemd_libdir}/system/*.target
%{systemd_libdir}/system/*.timer
%{systemd_libdir}/system/busnames.target.wants/*.busname
%{systemd_libdir}/system/graphical.target.wants/*.service
%{systemd_libdir}/system/local-fs.target.wants/*.mount
%{systemd_libdir}/system/local-fs.target.wants/*.service
%{systemd_libdir}/system/multi-user.target.wants/*.path
%{systemd_libdir}/system/multi-user.target.wants/*.service
%{systemd_libdir}/system/multi-user.target.wants/*.target
%{systemd_libdir}/system/rescue.target.wants/*.service
%{systemd_libdir}/system/sockets.target.wants/*.socket
%{systemd_libdir}/system/sysinit.target.wants/*.*mount
%{systemd_libdir}/system/sysinit.target.wants/*.path
%{systemd_libdir}/system/sysinit.target.wants/*.service
%{systemd_libdir}/system/sysinit.target.wants/*.target
%{systemd_libdir}/system/timers.target.wants/*.timer
%{systemd_libdir}/systemd*
%{systemd_libdir}/user-preset/*.preset
%{udev_libdir}/hwdb.d/*.hwdb
%{udev_rules_dir}/*.rules
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal
%attr(0755,root,root) /sbin/udevadm
%attr(0755,root,root) /sbin/udevd
%attr(0755,root,root) %{_bindir}/udevadm
%attr(0755,root,root) %{_sbindir}/udevadm
%attr(0755,root,root) %{udev_libdir}/accelerometer
%attr(0755,root,root) %{udev_libdir}/ata_id
%attr(0755,root,root) %{udev_libdir}/cdrom_id
%attr(0755,root,root) %{udev_libdir}/collect
%attr(0755,root,root) %{udev_libdir}/mtd_probe
%attr(0755,root,root) %{udev_libdir}/net_action
%attr(0755,root,root) %{udev_libdir}/net_create_ifcfg
%attr(0755,root,root) %{udev_libdir}/scsi_id
%attr(0755,root,root) %{udev_libdir}/udevd
%attr(0755,root,root) %{udev_libdir}/v4l_id
%config(noreplace) %{_prefix}/lib/sysctl.d/*.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/*.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
%config(noreplace) %{_sysconfdir}/rsyslog.d/listen.conf
%config(noreplace) %{_sysconfdir}/sysconfig/udev
%config(noreplace) %{_sysconfdir}/sysconfig/udev_net
%config(noreplace) %{_sysconfdir}/systemd/*.conf
%config(noreplace) %{_sysconfdir}/udev/*.conf

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/bin/systemctl
%{uclibc_root}/bin/systemd-ask-password
%{uclibc_root}/bin/systemd-escape
%{uclibc_root}/bin/systemd-firstboot
%{uclibc_root}/bin/systemd-hwdb
%{uclibc_root}/bin/systemd-notify
%{uclibc_root}/bin/systemd-tmpfiles
%{uclibc_root}/bin/systemd-tty-ask-password-agent
%{uclibc_root}/bin/journalctl
%{uclibc_root}/bin/loginctl
%{uclibc_root}/bin/systemd-inhibit
%{uclibc_root}/bin/systemd-machine-id-setup
%{uclibc_root}%{_bindir}/busctl
%{uclibc_root}%{_bindir}/bootctl
%{uclibc_root}%{_bindir}/kernel-install
%{uclibc_root}%{_bindir}/systemd-delta
%{uclibc_root}%{_bindir}/systemd-detect-virt
%{uclibc_root}%{_bindir}/systemd-loginctl
%{uclibc_root}%{_bindir}/systemd-run
%{uclibc_root}%{_bindir}/systemd-cgls
%{uclibc_root}%{_bindir}/systemd-nspawn
%{uclibc_root}%{_bindir}/systemd-stdio-bridge
%{uclibc_root}%{_bindir}/systemd-cat
%{uclibc_root}%{_bindir}/systemd-cgtop
%{uclibc_root}%{_bindir}/systemd-path
%attr(0755,root,root) %{uclibc_root}/bin/udevadm
%attr(0755,root,root) %{uclibc_root}/sbin/udevadm
%endif

%files journal-gateway
%config(noreplace) %{_sysconfdir}/systemd/journal-remote.conf
%config(noreplace) %{_sysconfdir}/systemd/journal-upload.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-remote.conf
%dir %{_datadir}/systemd/gatewayd
%{systemd_libdir}/systemd-journal-gatewayd
%{systemd_libdir}/systemd-journal-remote
%{systemd_libdir}/systemd-journal-upload
%{systemd_libdir}/system/systemd-journal-gatewayd.service
%{systemd_libdir}/system/systemd-journal-gatewayd.socket
%{systemd_libdir}/system/systemd-journal-remote.service
%{systemd_libdir}/system/systemd-journal-remote.socket
%{systemd_libdir}/system/systemd-journal-upload.service
%{_prefix}/lib/tmpfiles.d/systemd-remote.conf
%{_mandir}/man8/systemd-journal-gatewayd.8.*
%{_mandir}/man8/systemd-journal-upload.8.*
%{_mandir}/man8/systemd-journal-remote.8.*
%{_mandir}/man8/systemd-journal-gatewayd.service.8.*
%{_mandir}/man8/systemd-journal-gatewayd.socket.8.*
%{_datadir}/systemd/gatewayd/browse.html

%if !%{with bootstrap}
%files -n python-%{name} 
%{py_platsitedir}/%{name}
%endif

%files -n %{libnss_myhostname}
%{_libdir}/libnss_myhostname.so.%{libnss_major}*
%{_libdir}/libnss_mymachines.so.%{libnss_major}
%{_libdir}/libnss_resolve.so.%{libnss_major}
%{_mandir}/man8/libnss_myhostname.so*.8*
%{_mandir}/man8/libnss_mymachines.so*.8*
%{_mandir}/man8/nss-myhostname.8*
%{_mandir}/man8/nss-mymachines.8*

%if %{with uclibc}
%files -n uclibc-%{libnss_myhostname}
%{uclibc_root}%{_libdir}/libnss_myhostname.so.%{libnss_major}*
%endif

%files -n %{libsystemd}
/%{_lib}/libsystemd.so.%{libsystemd_major}*

%if %{with uclibc}
%files -n uclibc-%{libsystemd}
%{uclibc_root}/%{_lib}/libsystemd.so.%{libsystemd_major}*

%files -n uclibc-%{libsystemd_devel}
%{uclibc_root}%{_libdir}/libsystemd.so
%{uclibc_root}%{_libdir}/libsystemd.a
%endif

%files -n %{libsystemd_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/_sd-common.h
%{_includedir}/systemd/sd-bus-protocol.h
%{_includedir}/systemd/sd-bus-vtable.h
%{_includedir}/systemd/sd-bus.h
%{_includedir}/systemd/sd-event.h
%{_libdir}/libsystemd.so
%{_datadir}/pkgconfig/systemd.pc
%{_libdir}/pkgconfig/libsystemd.pc

%files -n %{libdaemon}
/%{_lib}/libsystemd-daemon.so.%{libdaemon_major}*

%if %{with uclibc}
%files -n uclibc-%{libdaemon}
%{uclibc_root}/%{_lib}/libsystemd-daemon.so.%{libdaemon_major}*

%files -n uclibc-%{libdaemon_devel}
%{uclibc_root}%{_libdir}/libsystemd-daemon.so
%{uclibc_root}%{_libdir}/libsystemd-daemon.a
%endif

%files -n %{libdaemon_devel}
%{_includedir}/systemd/sd-daemon.h
%{_libdir}/libsystemd-daemon.so
%{_libdir}/pkgconfig/libsystemd-daemon.pc
%{_includedir}/systemd/sd-messages.h

%files -n %{liblogin}
/%{_lib}/libsystemd-login.so.%{liblogin_major}*

%if %{with uclibc}
%files -n uclibc-%{liblogin}
%{uclibc_root}/%{_lib}/libsystemd-login.so.%{liblogin_major}*

%files -n uclibc-%{liblogin_devel}
%{uclibc_root}%{_libdir}/libsystemd-login.so
%{uclibc_root}%{_libdir}/libsystemd-login.a
%endif

%files -n %{liblogin_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-login.h
%{_libdir}/libsystemd-login.so
%{_libdir}/pkgconfig/libsystemd-login.pc

%files -n %{libjournal}
/%{_lib}/libsystemd-journal.so.%{libjournal_major}*

%if %{with uclibc}
%files -n uclibc-%{libjournal}
%{uclibc_root}/%{_lib}/libsystemd-journal.so.%{libjournal_major}*

%files -n uclibc-%{libjournal_devel}
%{uclibc_root}%{_libdir}/libsystemd-journal.so
%{uclibc_root}%{_libdir}/libsystemd-journal.a
%endif

%files -n %{libjournal_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-journal.h
%{_libdir}/libsystemd-journal.so
%{_libdir}/pkgconfig/libsystemd-journal.pc

%files -n %{libid128}
/%{_lib}/libsystemd-id128.so.%{libid128_major}*

%if %{with uclibc}
%files -n uclibc-%{libid128}
%{uclibc_root}/%{_lib}/libsystemd-id128.so.%{libid128_major}*

%files -n uclibc-%{libid128_devel}
%{uclibc_root}%{_libdir}/libsystemd-id128.so
%{uclibc_root}%{_libdir}/libsystemd-id128.a
%endif

%files -n %{libid128_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-id128.h
%{_libdir}/libsystemd-id128.so

%{_libdir}/pkgconfig/libsystemd-id128.pc

%files -n %{libudev}
/%{_lib}/libudev.so.%{udev_major}*

%if %{with uclibc}
%files -n uclibc-%{libudev}
%{uclibc_root}/%{_lib}/libudev.so.%{udev_major}*

%files -n uclibc-%{libudev_devel}
# do not remove static library, required by lvm2
%{uclibc_root}%{_libdir}/libudev.a
%{uclibc_root}%{_libdir}/libudev.so
%endif

%files -n %{libudev_devel}
%{_libdir}/libudev.so
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/udev.pc
%{_includedir}/libudev.h
