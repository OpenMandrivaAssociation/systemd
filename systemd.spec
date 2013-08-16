%bcond_with bootstrap
%bcond_without uclibc

# macros for sysvinit transition - should be equal to
# sysvinit %version-%release-plus-1
%define sysvinit_version 2.87
%define sysvinit_release %mkrel 18

%define libdaemon_major 0
%define liblogin_major 0
%define libjournal_major 0
%define libid128_major 0
%define libnss_myhostname_major 2

%define libdaemon %mklibname systemd-daemon %{libdaemon_major}
%define libdaemon_devel %mklibname -d systemd-daemon %{libdaemon_major}

%define liblogin %mklibname systemd-login %{liblogin_major}
%define liblogin_devel %mklibname -d systemd-login %{liblogin_major}

%define libjournal %mklibname systemd-journal %{libjournal_major}
%define libjournal_devel %mklibname -d systemd-journal %{libjournal_major}

%define libid128 %mklibname systemd-id128 %{libid128_major}
%define libid128_devel %mklibname -d systemd-id128 %{libid128_major}

%define libnss_myhostname %mklibname nss_myhostname %{libnss_myhostname_major}

%define udev_major 1
%define gudev_api 1.0
%define gudev_major 0
%define libudev %mklibname udev %{udev_major}
%define libudev_devel %mklibname udev -d
%define libgudev %mklibname gudev %{gudev_api} %{gudev_major}
%define libgudev_devel %mklibname gudev %{gudev_api} -d
%define girgudev %mklibname gudev-gir %{gudev_api}

%define systemd_libdir /lib/systemd
%define udev_libdir /lib/udev
%define udev_rules_dir %{udev_libdir}/rules.d
%define udev_user_rules_dir %{_sysconfdir}/udev/rules.d

Summary:	A System and Session Manager
Name:		systemd
Version:	206
Release:	3
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
Source1:	%{name}.macros
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
Source12:	99-default.preset
Source13:	systemd.rpmlintrc
### SYSTEMD ###

Patch1:		systemd-tmpfilesd-utmp-temp-patch.patch
#Patch2:		systemd-33-rc-local.patch
Patch3:		0502-main-Add-failsafe-to-the-sysvinit-compat-cmdline-key.patch
Patch5:		systemd-205-uclibc.patch
# We need a static libudev.a for the uClibc build because lvm2 requires it.
# Put back support for building it.
Patch6:		systemd-205-static.patch

# GIT

### UDEV ###
# from Mandriva
# disable coldplug for storage and device pci
Patch100:	udev-199-coldplug.patch
# (proyvind):	FIXME: setting udev_log to 'info' royally screws everything up
#		for some reason, revert to 'err' for now..
Patch104:	systemd-186-set-udev_log-to-err.patch
# uClibc lacks secure_getenv(), DO NOT REMOVE!
Patch105:	systemd-196-support-build-without-secure_getenv.patch
Patch106:	systemd-191-uclibc-no-mkostemp.patch
#Patch107:	systemd-191-link-against-librt.patch
# (tpg) https://bugs.freedesktop.org/show_bug.cgi?id=57887
# reverts commit http://cgit.freedesktop.org/systemd/systemd/commit?id=978cf3c75fbd94fd0e046206ada6169b35edd919
#Patch108:	systemd-197-dont-loose-active-session-after-su.patch

#Fedora patchset
# (tpg) disable for now
#Patch503: 0503-mandriva-Fallback-message-when-display-manager-fails.patch
#Patch504: 0504-mount-Add-a-new-remote-fs-target-to-specifically-del.patch
Patch506: 0506-Allow-booting-from-live-cd-in-virtualbox.patch
#Patch507: 0507-reinstate-TIMEOUT-handling.patch
Patch508: 0508-udev-Allow-the-udevadm-settle-timeout-to-be-set-via-.patch


BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	m4
BuildRequires:	libtool
BuildRequires:	acl-devel
BuildRequires:	audit-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	gperf
BuildRequires:	intltool
BuildRequires:	cap-devel
BuildRequires:	pam-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	tcp_wrappers-devel
BuildRequires:	vala >= 0.9
BuildRequires:	pkgconfig(dbus-1) >= 1.4.0
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	gtk-doc
%if !%{with bootstrap}
BuildRequires:	pkgconfig(libcryptsetup)
%endif
BuildRequires:	pkgconfig(libkmod) >= 5
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libqrencode)
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(blkid)
BuildRequires:	usbutils >= 005-3
BuildRequires:	pciutils-devel
BuildRequires:	ldetect-lst
BuildRequires:	python-devel
BuildRequires:	chkconfig

%if !%{with bootstrap}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%endif
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif
Requires(pre,post):	coreutils
Requires:	udev = %{version}-%{release}
Requires(post):	gawk
Requires(post):	grep
Requires(post):	awk
Requires:	dbus >= 1.3.2
Requires(pre):	initscripts > 9.24
Requires(pre):	basesystem-minimal
Requires(pre):	util-linux >= 2.18-2
Requires(pre):	rpm-helper
Requires(pre):	%{name}-units
Requires:	lockdev
Conflicts:	initscripts < 9.24
Conflicts:	udev < 186-5
%if "%{distepoch}" >= "2013.0"
#(tpg) time to drop consolekit stuff as it is replaced by native logind
Provides:	consolekit = 0.4.5-6
Provides:	consolekit-x11 = 0.4.5-6
Obsoletes:	consolekit <= 0.4.5-5
Obsoletes:	consolekit-x11 <= 0.4.5-5
Obsoletes:	libconsolekit0
Obsoletes:	lib64consolekit0
%endif
Requires:	kmod
%rename		readahead
Provides:	should-restart = system
# make sure we have /etc/os-release available, required by --with-distro
BuildRequires:	mandriva-release-common >= 1:2012.0-0.4
# (tpg) just to be sure we install this libraries
Requires:	libsystemd-daemon = %{version}-%{release}
Requires:	libsystemd-login = %{version}-%{release}
Requires:	libsystemd-journal = %{version}-%{release}
Requires:	libsystemd-id128 = %{version}-%{release}
Requires:	nss_myhostname = %{version}-%{release}
#(tpg)for future releases... systemd provides also a full functional syslog tool
Provides:	syslog-daemon

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
Requires:	uclibc-udev = %{EVRD}
Requires:	uclibc-%{libdaemon} = %{EVRD}
Requires:	uclibc-%{liblogin} = %{EVRD}
Requires:	uclibc-%{liblogin} = %{EVRD}
Requires:	uclibc-%{liblogin} = %{EVRD}

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

%package tools
Summary:	Non essential systemd tools
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name} < 35-6

%description tools
Non essential systemd tools.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		System/Configuration/Boot and Init
Requires(post):	coreutils
Requires(post):	gawk
Requires(post):	grep
Requires(post):	awk
Requires(pre):	setup
Requires(pre):	rpm-helper

%description units
Basic configuration files, directories and installation tool for the systemd
system and session manager.

%package sysvinit
Summary:	System V init tools
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{version}-%{release}
# (eugeni) systemd should work as a drop-in replacement for sysvinit, but not obsolete it
#SysVinit < %sysvinit_release-%sysvinit_release It's provides something
#like that SysVinit < 14-14 when it should be SysVinit 2.87-14
Provides:	sysvinit = %sysvinit_version-%sysvinit_release, SysVinit = %sysvinit_version-%sysvinit_release
# (tpg) time to die
Obsoletes:	sysvinit < %sysvinit_version-%sysvinit_release, SysVinit < %sysvinit_version-%sysvinit_release
# Due to halt/poweroff etc. in _bindir
Conflicts:	usermode-consoleonly < 1:1.110

%description sysvinit
Drop-in replacement for the System V init tools of systemd.

%package -n %{libdaemon}
Summary:	Systemd-daemon library package
Group:		System/Libraries
Provides:	libsystemd-daemon = %{version}-%{release}

%description -n	%{libdaemon}
This package provides the systemd-daemon shared library.

%if %{with uclibc}
%package -n	uclibc-%{libdaemon}
Summary:	Systemd-daemon library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libdaemon}
This package provides the systemd-daemon shared library.
%endif

%package -n %{libdaemon_devel}
Summary:	Systemd-daemon library development files
Group:		Development/C
Requires:	%{libdaemon} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libdaemon} = %{version}-%{release}
%endif
Provides:	libsystemd-daemon-devel = %{version}-%{release}

%description -n	%{libdaemon_devel}
Development files for the systemd-daemon shared library.

%package -n %{liblogin}
Summary:	Systemd-login library package
Group:		System/Libraries
Provides:	libsystemd-login = %{version}-%{release}

%description -n	%{liblogin}
This package provides the systemd-login shared library.

%package -n %{libnss_myhostname}
Summary:	Library for local system host name resolution
Group:		System/Libraries
Provides:	libnss_myhostname = %{version}-%{release}
Provides:	nss_myhostname = %{version}-%{release}
Obsoletes:	nss_myhostname <= 0.3-1
Requires(post,preun):	rpm-helper
Requires(post,preun):	sed

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

%if %{with uclibc}
%package -n uclibc-%{liblogin}
Summary:	Systemd-login library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{liblogin}
This package provides the systemd-login shared library.
%endif

%package -n %{liblogin_devel}
Summary:	Systemd-login library development files
Group:		Development/C
Requires:	%{liblogin} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{liblogin} = %{version}-%{release}
%endif
Provides:	libsystemd-login-devel = %{version}-%{release}

%description -n	%{liblogin_devel}
Development files for the systemd-login shared library.

%package -n %{libjournal}
Summary:	Systemd-journal library package
Group:		System/Libraries
Provides:	libsystemd-journal = %{version}-%{release}

%description -n	%{libjournal}
This package provides the systemd-journal shared library.

%if %{with uclibc}
%package -n uclibc-%{libjournal}
Summary:	Systemd-journal library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libjournal}
This package provides the systemd-journal shared library.
%endif

%package -n %{libjournal_devel}
Summary:	Systemd-journal library development files
Group:		Development/C
Requires:	%{libjournal} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libjournal} = %{version}-%{release}
%endif
Provides:	libsystemd-journal-devel = %{version}-%{release}

%description -n	%{libjournal_devel}
Development files for the systemd-journal shared library.

%package -n %{libid128}
Summary:	Systemd-id128 library package
Group:		System/Libraries
Provides:	libsystemd-id128 = %{version}-%{release}

%description -n	%{libid128}
This package provides the systemd-id128 shared library.

%if %{with uclibc}
%package -n uclibc-%{libid128}
Summary:	Systemd-id128 library package (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libid128}
This package provides the systemd-id128 shared library.
%endif

%package -n %{libid128_devel}
Summary:	Systemd-id128 library development files
Group:		Development/C
Requires:	%{libid128} = %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libid128} = %{version}-%{release}
%endif
Provides:	libsystemd-id128-devel = %{version}-%{release}

%description -n %{libid128_devel}
Development files for the systemd-id128 shared library.

%package -n udev
Summary:	Device manager for the Linux kernel
Group:		System/Configuration/Hardware
Requires:	%{name} = %{version}-%{release}
Requires:	ldetect-lst
Requires:	setup >= 2.7.16
Requires:	util-linux-ng >= 2.15
Requires:	acl
# for disk/lp groups
Requires(pre):	setup
Requires(pre):	coreutils
Requires(pre):	filesystem
Requires(pre):	rpm-helper
Requires(post,preun):	rpm-helper
Provides:	should-restart = system
Requires(post):	util-linux
Obsoletes:	hal	<= 0.5.14-6
# (tpg) moved form makedev package
Provides:	dev
Provides:	MAKEDEV
Conflicts:	makedev < 4.4-17

%description -n	udev
A collection of tools and a daemon to manage events received
from the kernel and deal with them in user-space. Primarily this
involves managing permissions, and creating and removing meaningful
symlinks to device nodes in /dev when hardware is discovered or
removed from the system

%if %{with uclibc}
%package -n uclibc-udev
Summary:	Device manager for the Linux kernel (uClibc linked)
Group:		System/Configuration/Hardware
Requires:	udev = %{EVRD}
#Requires:	ldetect-lst
#Requires:	setup >= 2.7.16
#Requires:	util-linux-ng >= 2.15
#Requires:	acl
# for disk/lp groups
#Requires(pre):	setup
#Requires(pre):	coreutils
#Requires(post,preun):	rpm-helper
#Provides:	should-restart = system

%description -n	uclibc-udev
A collection of tools and a daemon to manage events received
from the kernel and deal with them in user-space. Primarily this
involves managing permissions, and creating and removing meaningful
symlinks to device nodes in /dev when hardware is discovered or
removed from the system
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
%endif

%package -n %{libudev_devel}
Summary:	Devel library for udev
Group:		Development/C
License:	LGPLv2+
Provides:	udev-devel = %{EVRD}
Requires:	%{libudev} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libudev} = %{EVRD}
%endif
Obsoletes:	%{_lib}udev0-devel
Obsoletes:	%{name}-doc

%description -n	%{libudev_devel}
Devel library for udev.

%package -n %{libgudev}
Summary:	Libraries for adding libudev support to applications that use glib
Group:		System/Libraries
#gw please don't remove this again, it is needed by the noarch package
#gudev-sharp
Provides:	libgudev = %{EVRD}

%description -n	%{libgudev}
This package contains the libraries that make it easier to use libudev
functionality from applications that use glib.

%if !%{with bootstrap}
%package -n %{girgudev}
Group:		System/Libraries
Summary:	GObject Introspection interface library for gudev
Conflicts:	%{_lib}gudev1.0_0 < 182-5
Obsoletes:	%{_lib}udev-gir1.0

%description -n %{girgudev}
GObject Introspection interface library for gudev.
%endif

%package -n %{libgudev_devel}
Summary:	Header files for adding libudev support to applications that use glib
Group:		Development/C
Requires:	%{libgudev} = %{EVRD}

%description -n	%{libgudev_devel}
This package contains the header and pkg-config files for developing
glib-based applications using libudev functionality.

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
intltoolize --force --automake
autoreconf --force --install --symlink

%build
%serverbuild_hardened
%ifarch %arm
export ac_cv_func_malloc_0_nonnull=yes
%endif


export CONFIGURE_TOP="$PWD"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--prefix=%{_prefix} \
	--with-rootprefix= \
	--with-rootlibdir=%{uclibc_root}/%{_lib} \
	--libexecdir=%{_prefix}/lib \
	--with-firmware-path=/lib/firmware/updates:/lib/firmware \
	--enable-static \
	--with-sysvinit-path=%{_initrddir} \
	--with-sysvrcnd-path=%{_sysconfdir}/rc.d \
	--with-rc-local-script-path-start=/etc/rc.d/rc.local \
	--disable-selinux \
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
	--with-kbd-loadkeys=/bin/loadkeys \
	--with-kbd-setfont=/bin/setfont

%make
popd
%endif

mkdir -p shared
pushd shared
%configure2_5x \
	--with-rootprefix= \
	--with-rootlibdir=/%{_lib} \
	--libexecdir=%{_prefix}/lib \
	--with-firmware-path=/lib/firmware/updates:/lib/firmware \
	--disable-static \
	--with-distro=mandriva \
	--with-sysvinit-path=%{_initrddir} \
	--with-sysvrcnd-path=%{_sysconfdir}/rc.d \
	--with-rc-local-script-path-start=/etc/rc.d/rc.local \
	--disable-selinux \
%if %{with bootstrap}
	--enable-introspection=no \
	--disable-libcryptsetup \
%else
	--enable-introspection=yes \
%endif
	--enable-split-usr \
	--with-kbd-loadkeys=/bin/loadkeys \
	--with-kbd-setfont=/bin/setfont

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
ln -s ../bin/systemctl %{buildroot}/bin/reboot
ln -s ../bin/systemctl %{buildroot}/bin/halt
ln -s ../bin/systemctl %{buildroot}/bin/poweroff
ln -s ../bin/systemctl %{buildroot}/sbin/shutdown
ln -s ../bin/systemctl %{buildroot}/sbin/telinit
ln -s ../bin/systemctl %{buildroot}/sbin/runlevel
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
rm -f %{buildroot}%{_sysconfdir}/systemd/system/display-manager.service

# Make sure these directories are properly owned
mkdir -p %{buildroot}/%{systemd_libdir}/system/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/dbus.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/syslog.target.wants

#(tpg) keep these compat symlink
ln -s %{systemd_libdir}/system/systemd-udevd.service %{buildroot}/%{systemd_libdir}/system/udev.service
ln -s %{systemd_libdir}/system/systemd-udev-settle.service %{buildroot}/%{systemd_libdir}/system/udev-settle.service

# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/systemd/system/default.target

# (tpg) this is needed
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-generators
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user-generators

# We are not prepared to deal with tmpfs /var/run or /var/lock
pushd %{buildroot}/%{systemd_libdir}/system/local-fs.target.wants && {
 rm -f var-lock.mount
 rm -f var-run.mount
popd
}

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}/%{systemd_libdir}/system/bluetooth.target.wants

# (tpg) use systemd's own mounting capability
sed -i -e 's/^#MountAuto=yes$/MountAuto=yes/' %{buildroot}/etc/systemd/system.conf
sed -i -e 's/^#SwapAuto=yes$/SwapAuto=yes/' %{buildroot}/etc/systemd/system.conf

# (bor) enable rpcbind.target by default so we have something to plug portmapper service into
ln -s ../rpcbind.target %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants

# (bor) machine-id-setup is in /sbin in post-v20
install -d %{buildroot}/sbin && mv %{buildroot}/bin/systemd-machine-id-setup %{buildroot}/sbin
%if %{with uclibc}
install -d %{buildroot}%{uclibc_root}/sbin && mv %{buildroot}%{uclibc_root}/bin/systemd-machine-id-setup %{buildroot}%{uclibc_root}/sbin
%endif


# (eugeni) install /run
mkdir %{buildroot}/run

# (tpg) create missing dir
mkdir -p %{buildroot}%{_libdir}/systemd/user/

# add missing ttys (mdv #63600)
mkdir -p %{buildroot}/etc/systemd/system/getty.target.wants
pushd %{buildroot}/etc/systemd/system/getty.target.wants
	for _term in 1 2 3 4 5 6 ; do
	ln -s %{systemd_libdir}/system/getty@.service getty@tty$_term.service
	done
popd

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

# (tpg) add rpm macros
install -m 0644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d/%{name}.macros

# Make sure the NTP units dir exists
mkdir -p %{buildroot}%{systemd_libdir}/ntp-units.d/
install -m 0755 -d %{buildroot}%{_logdir}/journal

# (tpg) Install default Mandriva preset policy for services
mkdir -p %{buildroot}%{systemd_libdir}/system-preset/
mkdir -p %{buildroot}%{systemd_libdir}/user-preset/
install -m 0644 %{SOURCE12} %{buildroot}%{systemd_libdir}/system-preset/

# Install rsyslog fragment
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/rsyslog.d/

# (tpg) from mageia
# automatic systemd release on rpm installs/removals
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
install -d %{buildroot}%{_var}/lib/rpm/filetriggers
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.filter << EOF
^./lib/systemd/system/
^./etc/systemd/system/
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.script << EOF
#!/bin/sh
if /bin/mountpoint -q /sys/fs/cgroup/systemd; then
    if [ -x /bin/systemctl ]; then
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
    fi
fi
EOF
chmod 755 %{buildroot}%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.script
# (tpg) silent kernel messages
# print only KERN_ERR and more serious alerts
echo "kernel.printk = 3 3 3 3" >> %{buildroot}/usr/lib/sysctl.d/50-default.conf

#################
#	UDEV	#
#	START	#
#################

install -m 644 %{SOURCE2} %{buildroot}%{udev_rules_dir}/
install -m 644 %{SOURCE3} %{buildroot}%{udev_rules_dir}/
install -m 0644 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/sysconfig/udev
# net rules
install -m 0644 %{SOURCE6} %{buildroot}%{udev_rules_dir}/
install -m 0755 %{SOURCE7} %{buildroot}%{udev_libdir}/net_create_ifcfg
install -m 0755 %{SOURCE8} %{buildroot}%{udev_libdir}/net_action
install -m 0644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/udev_net

# disable "predictable network interface names" for now..
# ref: http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames
ln -s /dev/null %{buildroot}%{udev_user_rules_dir}/80-net-name-slot.rules

install -m 0644 %{SOURCE10} %{buildroot}%{udev_rules_dir}/

# probably not required, but let's just be on the safe side for now..
ln -sf /bin/udevadm %{buildroot}/sbin/udevadm
ln -sf /bin/udevadm %{buildroot}%{_bindir}/udevadm
ln -sf /bin/udevadm %{buildroot}%{_sbindir}/udevadm

# (tpg) this is needed, because udevadm is in /bin
# altering the path allows to boot on before root pivot
sed -i -e 's#/usr/bin/udevadm#/bin/udevadm#g' %{buildroot}/%{systemd_libdir}/system/*.service

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

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 -o $2 -ge 2 ] ; then
	/bin/systemctl daemon-reexec 2>&1 || :
fi

%pre -n udev
if [ -d /lib/hotplug/firmware ]; then
	echo "Moving /lib/hotplug/firmware to /lib/firmware"
	mkdir -p /lib/firmware
	mv /lib/hotplug/firmware/* /lib/firmware/ 2>/dev/null
	rmdir -p --ignore-fail-on-non-empty /lib/hotplug/firmware
	:
fi

%post -n udev
/bin/systemctl --quiet try-restart systemd-udevd.service >/dev/null 2>&1 || :

#%post -n uclibc-udev
#%{uclibc_root}/bin/systemctl --quiet try-restart systemd-udevd.service >/dev/null 2>&1 || :

%pre
%_pre_groupadd systemd-journal systemd-journal
%_pre_useradd systemd-journal-gateway %{_var}/run/%{name}-journal-gateway /bin/false
%_pre_groupadd systemd-journal-gateway systemd-journal-gateway
systemctl stop stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :

%post
/usr/bin/systemd-machine-id-setup >/dev/null 2>&1 || :
/usr/lib/systemd/systemd-random-seed save >/dev/null 2>&1 || :
/usr/bin/systemctl daemon-reexec >/dev/null 2>&1 || :
/usr/bin/systemctl start systemd-udevd.service >/dev/null 2>&1 || :
/bin/udevadm hwdb --update >/dev/null 2>&1 || :
/usr/bin/journalctl --update-catalog >/dev/null 2>&1 || :

# (tpg) this is needed for rsyslog
/bin/ln -s /usr/lib/systemd/system/rsyslog.service /etc/systemd/system/syslog.service >/dev/null 2>&1 || :

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
        [ -n "$LANG" ] && echo LANG=$LANG > /etc/locale.conf 2>&1 || :
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

# Migrate /etc/sysconfig/keyboard
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

# Migrate HOSTNAME= from /etc/sysconfig/network
if [ -e /etc/sysconfig/network -a ! -e /etc/hostname ]; then
        unset HOSTNAME
        . /etc/sysconfig/network >/dev/null 2>&1 || :
        [ -n "$HOSTNAME" ] && echo $HOSTNAME > /etc/hostname 2>&1 || :
fi
/usr/bin/sed -i '/^HOSTNAME=/d' /etc/sysconfig/network >/dev/null 2>&1 || :

# Migrate the old systemd-setup-keyboard X11 configuration fragment
if [ ! -e /etc/X11/xorg.conf.d/00-keyboard.conf ] ; then
        /usr/bin/mv /etc/X11/xorg.conf.d/00-system-setup-keyboard.conf /etc/X11/xorg.conf.d/00-keyboard.conf >/dev/null 2>&1 || :
else
        /usr/bin/rm -f /etc/X11/xorg.conf.d/00-system-setup-keyboard.conf >/dev/null 2>&1 || :
fi

# sed-fu to add myhostname to the hosts line of /etc/nsswitch.conf
if [ -f /etc/nsswitch.conf ] ; then
        sed -i.bak -e '
                /^hosts:/ !b
                /\<myhostname\>/ b
                s/[[:blank:]]*$/ myhostname/
                ' /etc/nsswitch.conf
fi

%triggerin units -- %{name}-units < 35-1
# Enable the services we install by default.
/bin/systemctl --quiet enable \
	hwclock-load.service \
    getty@tty1.service \
	quotaon.service \
	quotacheck.service \
	remote-fs.target
	systemd-readahead-replay.service \
	systemd-readahead-collect.service \
	2>&1 || :
# rc-local is now enabled by default in base package
rm -f /etc/systemd/system/multi-user.target.wants/rc-local.service || :

#systemd 195 changed the prototype of logind's OpenSession()
# see http://lists.freedesktop.org/archives/systemd-devel/2012-October/006969.html
# and http://cgit.freedesktop.org/systemd/systemd/commit/?id=770858811930c0658b189d980159ea1ac5663467
%triggerun -- %{name} < 196
%{_bindir}/systemctl restart systemd-logind.service

%post units
if [ $1 -eq 1 ] ; then
        # Try to read default runlevel from the old inittab if it exists
        runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
        if [ -z "$runlevel" ] ; then
                target="/lib/systemd/system/graphical.target"
        else
                target="/lib/systemd/system/runlevel$runlevel.target"
        fi

        # And symlink what we found to the new-style default.target
        /bin/ln -sf "$target" %{_sysconfdir}/systemd/system/default.target 2>&1 || :

        # Enable the services we install by default.
        /bin/systemctl --quiet enable \
                getty@tty1.service \
                remote-fs.target \
                systemd-readahead-replay.service \
                systemd-readahead-collect.service \
                2>&1 || :
fi

hostname_new=`cat %{_sysconfdir}/hostname 2>/dev/null`
if [ -z $hostname_new ]; then
        hostname_old=`cat /etc/sysconfig/network 2>/dev/null | grep HOSTNAME | cut -d "=" -f2`
	if [ ! -z $hostname_old ]; then
    		echo $hostname_old >> %{_sysconfdir}/hostname
        else
    		echo "localhost" >> %{_sysconfdir}/hostname
        fi
fi

%preun units
if [ $1 -eq 0 ] ; then
        /bin/systemctl --quiet disable \
		getty@.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service \
		systemd-udev-settle.service \
		2>&1 || :

        /bin/rm -f /etc/systemd/system/default.target 2>&1 || :
fi

%postun units
if [ $1 -ge 1 ] ; then
        /bin/systemctl daemon-reload 2>&1 || :
fi


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


%files
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%config(noreplace) %{_sysconfdir}/rsyslog.d/listen.conf
%config(noreplace) /usr/lib/sysctl.d/50-coredump.conf
%config(noreplace) /usr/lib/sysctl.d/50-default.conf
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%ghost %{_sysconfdir}/udev/hwdb.bin

%dir /run
%dir %{systemd_libdir}
%dir %{systemd_libdir}/*-generators
%dir %{systemd_libdir}/system-shutdown
%dir %{systemd_libdir}/system-sleep
%dir %{systemd_libdir}/ntp-units.d
%dir %{systemd_libdir}/system-preset
%dir %{systemd_libdir}/user-preset
%dir %{_datadir}/systemd
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/binfmt.d
%dir %{_logdir}/journal
%dir %{_datadir}/systemd/gatewayd

%{_sysconfdir}/xdg/systemd
/bin/systemd-ask-password
/bin/systemd-notify
/bin/systemd-tmpfiles
/bin/systemd-tty-ask-password-agent
/bin/systemd
/bin/journalctl
/bin/loginctl
/bin/systemd-inhibit
/sbin/systemd-machine-id-setup
%{_bindir}/systemd-delta
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-loginctl
%{_bindir}/systemd-run
%{_bindir}/hostnamectl
%{_bindir}/localectl
%{_bindir}/kernel-install
%{_bindir}/bootctl
%{_bindir}/systemd-coredumpctl
%{_bindir}/timedatectl
%{_prefix}/lib/kernel/install.d/*.install
%{systemd_libdir}/systemd
%{systemd_libdir}/systemd-ac-power
%{systemd_libdir}/systemd-activate
%{systemd_libdir}/systemd-bootchart
%{systemd_libdir}/systemd-binfmt
%{systemd_libdir}/systemd-c*
%{systemd_libdir}/systemd-fsck
%{systemd_libdir}/systemd-hostnamed
%{systemd_libdir}/systemd-initctl
%{systemd_libdir}/systemd-journal*
%{systemd_libdir}/systemd-lo*
%{systemd_libdir}/systemd-m*
%{systemd_libdir}/systemd-quotacheck
%{systemd_libdir}/systemd-random-seed
%{systemd_libdir}/systemd-re*
%{systemd_libdir}/systemd-s*
%{systemd_libdir}/systemd-time*
%{systemd_libdir}/systemd-update-utmp
%{systemd_libdir}/systemd-user-sessions
%{systemd_libdir}/systemd-vconsole-setup
%{systemd_libdir}/*-generators/*
%{systemd_libdir}/system-preset/99-default.preset
/usr/lib/tmpfiles.d/*.conf
/%{_lib}/security/pam_systemd.so
%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.*
%{_bindir}/systemd-cgls
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgtop
%{_mandir}/man1/systemd.*
%{_mandir}/man1/systemd-ask-password.*
%{_mandir}/man1/systemd-bootchart.1.*
%{_mandir}/man1/systemd-tty-ask-password-agent.*
%{_mandir}/man1/systemd-cat.1*
%{_mandir}/man1/systemd-cgls.*
%{_mandir}/man1/systemd-cgtop.*
%{_mandir}/man1/systemd-coredumpctl.1.*
%{_mandir}/man1/hostnamectl.*
%{_mandir}/man1/journalctl.1*
%{_mandir}/man1/localectl.*
%{_mandir}/man1/loginctl.*
%{_mandir}/man1/systemd-run.1.*
%{_mandir}/man1/systemd-machine-id-setup.1*
%{_mandir}/man1/systemd-notify.*
%{_mandir}/man1/systemd-nspawn.*
%{_mandir}/man1/systemd-delta.1.*
%{_mandir}/man1/systemd-detect-virt.1.*
%{_mandir}/man1/systemd-inhibit.1.*
%{_mandir}/man1/timedatectl.*
%{_mandir}/man1/machinectl.1.*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/pam_systemd.*
%{_mandir}/man8/systemd-*
%{_mandir}/man8/kernel-install.*
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.hostname1*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.locale1*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.timedate1*.xml
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_datadir}/systemd/kbd-model-map
%{_docdir}/systemd
%{_datadir}/systemd/gatewayd/browse.html

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/bin/machinectl
%{uclibc_root}/bin/systemctl
%{uclibc_root}/bin/systemd-ask-password
%{uclibc_root}/bin/systemd-notify
%{uclibc_root}/bin/systemd-tmpfiles
%{uclibc_root}/bin/systemd-tty-ask-password-agent
%{uclibc_root}/bin/journalctl
%{uclibc_root}/bin/loginctl
%{uclibc_root}/bin/systemd-inhibit
%{uclibc_root}/sbin/systemd-machine-id-setup
%{uclibc_root}%{_bindir}/hostnamectl
%{uclibc_root}%{_bindir}/localectl
%{uclibc_root}%{_bindir}/bootctl
%{uclibc_root}%{_bindir}/kernel-install
%{uclibc_root}%{_bindir}/systemd-coredumpctl
%{uclibc_root}%{_bindir}/systemd-delta
%{uclibc_root}%{_bindir}/systemd-detect-virt
%{uclibc_root}%{_bindir}/systemd-loginctl
%{uclibc_root}%{_bindir}/systemd-run
%{uclibc_root}%{_bindir}/systemd-cgls
%{uclibc_root}%{_bindir}/systemd-nspawn
%{uclibc_root}%{_bindir}/systemd-stdio-bridge
%{uclibc_root}%{_bindir}/systemd-cat
%{uclibc_root}%{_bindir}/systemd-cgtop
%{uclibc_root}%{_bindir}/timedatectl
%endif

%files tools
%{_bindir}/systemd-analyze
%{_mandir}/man1/systemd-analyze.1*
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/*.py*
%{python_sitearch}/%{name}/*.so

%files units
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/system/getty.target.wants
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions

%{_sysconfdir}/systemd/system/getty.target.wants/getty@*.service
%{_datadir}/bash-completion/completions/*

/bin/systemctl
%{_bindir}/systemctl
/bin/machinectl
%{systemd_libdir}/system
/usr/lib/systemd/
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/rpm/macros.d/%{name}.macros
%{_prefix}/lib/rpm/macros.d/macros.systemd
%{_mandir}/man1/systemctl.*

%files sysvinit
/sbin/init
/bin/reboot
/bin/halt
/bin/poweroff
/sbin/shutdown
/sbin/telinit
/sbin/runlevel
%{_initrddir}/README
%{_logdir}/README
%{_mandir}/man1/init.*
%{_mandir}/man8/halt.*
%{_mandir}/man8/reboot.*
%{_mandir}/man8/shutdown.*
%{_mandir}/man8/poweroff.*
%{_mandir}/man8/telinit.*
%{_mandir}/man8/runlevel.*
%dir /run

%files -n %{libnss_myhostname}
%{_libdir}/libnss_myhostname.so.%{libnss_myhostname_major}*
%{_mandir}/man8/nss-myhostname.8*

%if %{with uclibc}
%files -n uclibc-%{libnss_myhostname}
%{uclibc_root}%{_libdir}/libnss_myhostname.so.%{libnss_myhostname_major}*
%endif

%files -n %{libdaemon}
/%{_lib}/libsystemd-daemon.so.%{libdaemon_major}*

%if %{with uclibc}
%files -n uclibc-%{libdaemon}
%{uclibc_root}/%{_lib}/libsystemd-daemon.so.%{libdaemon_major}*
%endif

%files -n %{libdaemon_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-daemon.h
%{_libdir}/libsystemd-daemon.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libsystemd-daemon.so
%{uclibc_root}%{_libdir}/libsystemd-daemon.a
%endif
%{_libdir}/pkgconfig/libsystemd-daemon.pc
%{_datadir}/pkgconfig/systemd.pc
%{_includedir}/systemd/sd-messages.h
%{_includedir}/systemd/sd-shutdown.h

%files -n %{liblogin}
/%{_lib}/libsystemd-login.so.%{liblogin_major}*

%if %{with uclibc}
%files -n uclibc-%{liblogin}
%{uclibc_root}/%{_lib}/libsystemd-login.so.%{liblogin_major}*
%endif

%files -n %{liblogin_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-login.h
%{_libdir}/libsystemd-login.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libsystemd-login.so
%{uclibc_root}%{_libdir}/libsystemd-login.a
%endif
%{_libdir}/pkgconfig/libsystemd-login.pc

%files -n %{libjournal}
/%{_lib}/libsystemd-journal.so.%{libjournal_major}*

%if %{with uclibc}
%files -n uclibc-%{libjournal}
%{uclibc_root}/%{_lib}/libsystemd-journal.so.%{libjournal_major}*
%endif

%files -n %{libjournal_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-journal.h
%{_libdir}/libsystemd-journal.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libsystemd-journal.so
%{uclibc_root}%{_libdir}/libsystemd-journal.a
%endif
%{_libdir}/pkgconfig/libsystemd-journal.pc

%files -n %{libid128}
/%{_lib}/libsystemd-id128.so.%{libid128_major}*

%if %{with uclibc}
%files -n uclibc-%{libid128}
%{uclibc_root}/%{_lib}/libsystemd-id128.so.%{libid128_major}*
%endif

%files -n %{libid128_devel}
%dir %{_includedir}/systemd
%{_includedir}/systemd/sd-id128.h
%{_libdir}/libsystemd-id128.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libsystemd-id128.so
%{uclibc_root}%{_libdir}/libsystemd-id128.a
%endif
%{_libdir}/pkgconfig/libsystemd-id128.pc

%files -n udev
%dir /lib/firmware
%dir /lib/firmware/updates
%dir %{udev_libdir}
%dir %{udev_libdir}/hwdb.d
%dir %{_sysconfdir}/udev
%dir %{udev_rules_dir}
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/agents.d
%dir %{_sysconfdir}/udev/agents.d/usb
%config(noreplace) %{_sysconfdir}/sysconfig/udev
%config(noreplace) %{_sysconfdir}/sysconfig/udev_net
%config(noreplace) %{_sysconfdir}/udev/*.conf
%{udev_user_rules_dir}/80-net-name-slot.rules
%ghost %config(noreplace,missingok) %attr(0644,root,root) %{_sysconfdir}/scsi_id.config

%{systemd_libdir}/systemd-udevd
/bin/udevadm
%attr(0755,root,root) /sbin/udevadm
%attr(0755,root,root) %{_sbindir}/udevadm
%attr(0755,root,root) %{_bindir}/udevadm
%attr(0755,root,root) /sbin/udevd
%attr(0755,root,root) %{udev_libdir}/udevd
%{udev_libdir}/hwdb.d/*.hwdb
%{udev_rules_dir}/*.rules

%attr(0755,root,root) %{udev_libdir}/accelerometer
%attr(0755,root,root) %{udev_libdir}/ata_id
%attr(0755,root,root) %{udev_libdir}/cdrom_id
%attr(0755,root,root) %{udev_libdir}/scsi_id
%attr(0755,root,root) %{udev_libdir}/collect
%attr(0755,root,root) %{udev_libdir}/net_create_ifcfg
%attr(0755,root,root) %{udev_libdir}/net_action
%attr(0755,root,root) %{udev_libdir}/v4l_id
%attr(0755,root,root) %{udev_libdir}/mtd_probe

# From previous Mandriva /etc/udev/devices.d and patches
%attr(0666,root,root) %dev(c,1,3) %{udev_libdir}/devices/null
%attr(0600,root,root) %dev(b,2,0) %{udev_libdir}/devices/fd0
%attr(0600,root,root) %dev(b,2,1) %{udev_libdir}/devices/fd1
%attr(0600,root,root) %dev(c,21,0) %{udev_libdir}/devices/sg0
%attr(0600,root,root) %dev(c,21,1) %{udev_libdir}/devices/sg1
%attr(0600,root,root) %dev(c,9,0) %{udev_libdir}/devices/st0
%attr(0600,root,root) %dev(c,9,1) %{udev_libdir}/devices/st1
%attr(0600,root,root) %dev(c,99,0) %{udev_libdir}/devices/parport0
%dir %{udev_libdir}/devices/cpu
%dir %{udev_libdir}/devices/cpu/0
%attr(0600,root,root) %dev(c,203,0) %{udev_libdir}/devices/cpu/0/cpuid
%attr(0600,root,root) %dev(c,10,184) %{udev_libdir}/devices/cpu/0/microcode
%attr(0600,root,root) %dev(c,202,0) %{udev_libdir}/devices/cpu/0/msr
%attr(0600,root,root) %dev(c,162,0) %{udev_libdir}/devices/rawctl
%attr(0600,root,root) %dev(c,195,0) %{udev_libdir}/devices/nvidia0
%attr(0600,root,root) %dev(c,195,255) %{udev_libdir}/devices/nvidiactl
# Default static nodes to copy to /dev on udevd start
%dir %{udev_libdir}/devices
# From Fedora RPM
%attr(0755,root,root) %dir %{udev_libdir}/devices/net
%attr(0755,root,root) %dir %{udev_libdir}/devices/hugepages
%attr(0755,root,root) %dir %{udev_libdir}/devices/pts
%attr(0755,root,root) %dir %{udev_libdir}/devices/shm
%attr(666,root,root) %dev(c,10,200) %{udev_libdir}/devices/net/tun
%attr(600,root,root) %dev(c,108,0) %{udev_libdir}/devices/ppp
%attr(666,root,root) %dev(c,10,229) %{udev_libdir}/devices/fuse
%attr(660,root,lp) %dev(c,6,0) %{udev_libdir}/devices/lp0
%attr(660,root,lp) %dev(c,6,1) %{udev_libdir}/devices/lp1
%attr(660,root,lp) %dev(c,6,2) %{udev_libdir}/devices/lp2
%attr(660,root,lp) %dev(c,6,3) %{udev_libdir}/devices/lp3
%attr(640,root,disk) %dev(b,7,0) %{udev_libdir}/devices/loop0
%attr(640,root,disk) %dev(b,7,1) %{udev_libdir}/devices/loop1
%attr(640,root,disk) %dev(b,7,2) %{udev_libdir}/devices/loop2
%attr(640,root,disk) %dev(b,7,3) %{udev_libdir}/devices/loop3
%attr(640,root,disk) %dev(b,7,4) %{udev_libdir}/devices/loop4
%attr(640,root,disk) %dev(b,7,5) %{udev_libdir}/devices/loop5
%attr(640,root,disk) %dev(b,7,6) %{udev_libdir}/devices/loop6
%attr(640,root,disk) %dev(b,7,7) %{udev_libdir}/devices/loop7
%{_mandir}/man8/udevadm.8.*

%if %{with uclibc}
%files -n uclibc-udev
%attr(0755,root,root) %{uclibc_root}/bin/udevadm
%attr(0755,root,root) %{uclibc_root}/sbin/udevadm
%endif

%files -n %{libudev}
/%{_lib}/libudev.so.%{udev_major}*

%if %{with uclibc}
%files -n uclibc-%{libudev}
%{uclibc_root}/%{_lib}/libudev.so.%{udev_major}*
%endif

%files -n %{libudev_devel}
%{_libdir}/libudev.so
%if %{with uclibc}
# do not remove static library, required by lvm2
%{uclibc_root}%{_libdir}/libudev.a
%{uclibc_root}%{_libdir}/libudev.so
%endif
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/udev.pc
%{_includedir}/libudev.h

%files -n %{libgudev}
/%{_lib}/libgudev-%{gudev_api}.so.%{gudev_major}*

%files -n %{libgudev_devel}
%{_libdir}/libgudev-%{gudev_api}.so
%{_includedir}/gudev-%{gudev_api}
%if !%{with bootstrap}
%{_datadir}/gir-1.0/GUdev-%{gudev_api}.gir
%endif
%{_libdir}/pkgconfig/gudev-%{gudev_api}.pc

%if !%{with bootstrap}
%files -n %{girgudev}
%{_libdir}/girepository-1.0/GUdev-%{gudev_api}.typelib
%endif
