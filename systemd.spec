# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# FIXME workaround for a very very weird bug
# systemd on x86_64, but not znver1 (so we're intentionally
# not using %{x86_64} here), hangs indefinitely on upgrades
# if built with clang.
# Last verified with systemd 246.20200806, clang 10.0.1
# aarch64 added for testing (to see if systemctl hangs on
# synquacer and pinephone go away)
%ifarch x86_64 aarch64
%bcond_with gcc
%else
%bcond_with gcc
%endif

# (tpg) special options for systemd to keep it fast and secure
%if %{with gcc}
%ifnarch %{ix86}
%global optflags %{optflags} -fexceptions -fstack-protector --param=ssp-buffer-size=32 -fPIC
%else
%global optflags %{optflags} -fexceptions -fstack-protector --param=ssp-buffer-size=32 -fPIC -fuse-ld=bfd
%global ldflags %{ldflags} -fuse-ld=bfd -fPIC
%endif
%else
%ifnarch %{ix86}
%global optflags %{optflags} -fexceptions -fstack-protector --param=ssp-buffer-size=32
%else
%global optflags %{optflags} -fexceptions -fstack-protector --param=ssp-buffer-size=32 -fuse-ld=bfd
%global ldflags %{ldflags} -fuse-ld=bfd
%endif
%endif

%bcond_with bootstrap

# (tpg) do not reqire pkg-config
%global __requires_exclude pkg-config

%define libsystemd_major 0
%define libnss_major 2

%define libsystemd %mklibname %{name} %{libsystemd_major}
%define libsystemd_devel %mklibname %{name} -d
%define lib32systemd lib%{name}%{libsystemd_major}
%define lib32systemd_devel lib%{name}-devel

%define libnss_myhostname %mklibname nss_myhostname %{libnss_major}
%define libnss_mymachines %mklibname nss_mymachines %{libnss_major}
%define libnss_resolve %mklibname nss_resolve %{libnss_major}
%define libnss_systemd %mklibname nss_systemd %{libnss_major}
%define lib32nss_myhostname libnss_myhostname%{libnss_major}
%define lib32nss_systemd libnss_systemd%{libnss_major}

%define udev_major 1
%define libudev %mklibname udev %{udev_major}
%define libudev_devel %mklibname udev -d
%define lib32udev libudev%{udev_major}
%define lib32udev_devel libudev-devel

%define systemd_libdir /lib/systemd
%define udev_libdir /lib/udev
%define udev_rules_dir %{udev_libdir}/rules.d
%define udev_user_rules_dir %{_sysconfdir}/udev/rules.d

%define major 247
%define stable 20210305

Summary:	A System and Session Manager
Name:		systemd
%if 0%stable
Version:	%{major}.%{stable}
# Packaged from v%(echo %{version} |cut -d. -f1)-stable branch of
# git clone https://github.com/systemd/systemd-stable/ -b v247-stable
# cd systemd-stabe && git archive --prefix=systemd-247.$(date +%Y%m%d)/ --format=tar v247-stable | xz -9ef > ../systemd-247.$(date +%Y%m%d).tar.xz
Source0:	systemd-%{version}.tar.xz
%else
Version:	%{major}
Source0:	https://github.com/systemd/systemd/archive/v%{version}.tar.gz
%endif
Release:	1
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
# This file must be available before %%prep.
# It is generated during systemd build and can be found in src/core/.
Source1:	triggers.systemd
Source2:	50-udev-mandriva.rules
Source3:	69-printeracl.rules
Source5:	udev.sysconfig
# (blino) net rules and helpers
Source11:	listen.conf
# (tpg) default preset for services
Source12:	99-default-disable.preset
Source13:	90-default.preset
Source14:	85-display-manager.preset
Source16:	systemd.rpmlintrc
# (crazy) don't play weird games with these
# never enable / disable like this
#Source18:	90-user-default.preset
Source19:	10-imx.rules
# (tpg) EFI bootctl
Source21:	efi-loader.conf
Source22:	efi-omv.conf

Source23:	systemd-udev-trigger-no-reload.conf
# (tpg) protect systemd from unistnalling it
Source24:	yum-protect-systemd.conf

### OMV patches###
# disable coldplug for storage and device pci (nokmsboot/failsafe boot option required for proprietary video driver handling)
Patch2:		0503-Disable-modprobe-pci-devices-on-coldplug-for-storage.patch
Patch5:		systemd-216-set-udev_log-to-err.patch
Patch8:		systemd-206-set-max-journal-size-to-150M.patch
Patch9:		systemd-245-disable-audit-by-default.patch
Patch11:	systemd-220-silent-fsck-on-boot.patch
Patch14:	systemd-217-do-not-run-systemd-firstboot-in-containers.patch
Patch15:	0500-create-default-links-for-primary-cd_dvd-drive.patch
Patch17:	0515-Add-path-to-locale-search.patch
Patch18:	0516-udev-silence-version-print.patch
Patch19:	systemd-243-random-seed-no-insane-timeouts.patch
Patch20:	http://crazy.dev.frugalware.org/fix-macros.systemd.in.patch

# (tpg) ClearLinux patches
Patch100:	0001-journal-raise-compression-threshold.patch
Patch101:	0002-journal-Add-option-to-skip-boot-kmsg-events.patch
Patch102:	0003-core-use-mmap-to-load-files.patch
Patch103:	0005-journal-flush-var-kmsg-after-starting-disable-kmsg-f.patch
Patch104:	0007-sd-event-return-malloc-memory-reserves-when-main-loo.patch
Patch105:	0008-efi-boot-generator-Do-not-automount-boot-partition.patch
Patch106:	0010-locale-setup-set-default-locale-to-a-unicode-one.patch
Patch107:	0016-tmpfiles-Make-var-cache-ldconfig-world-readable.patch
Patch108:	0018-more-udev-children-workers.patch
Patch109:	0019-not-load-iptables.patch
Patch110:	0023-DHCP-retry-faster.patch
Patch111:	0024-Remove-libm-memory-overhead.patch
Patch112:	0028-Make-timesyncd-a-simple-service.patch
Patch113:	0029-Compile-udev-with-O3.patch
Patch114:	0030-Don-t-wait-for-utmp-at-shutdown.patch
Patch115:	0031-Don-t-do-transient-hostnames-we-set-ours-already.patch
Patch116:	0032-don-t-use-libm-just-for-integer-exp10.patch
Patch117:	0033-Notify-systemd-earlier-that-resolved-is-ready.patch
Patch118:	0035-skip-not-present-ACPI-devices.patch
Patch119:	0037-Disable-XZ-support-in-the-journal.patch
Patch120:	0038-Localize-1-symbol.patch

# (tpg) OMV patches
Patch1000:	systemd-236-fix-build-with-LLVM.patch
Patch1001:	systemd-245-allow-compiling-with-gcc.patch
#(tpg) we use bsdtar so let's adapt attribues to match implementation
# httpa://github.com/systemd/systemd/issues/16506
Patch1002:	systemd-245-importctl-fix-bsdtar-attributes.patch

# (tpg) Fedora patches
Patch1100:	0998-resolved-create-etc-resolv.conf-symlink-at-runtime.patch

# Upstream patches from master that haven't landed in -stable yet
BuildRequires:	meson
BuildRequires:	quota
BuildRequires:	audit-devel
BuildRequires:	pkgconfig(libacl)
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	gperf
BuildRequires:	intltool
BuildRequires:	cap-devel
BuildRequires:	pam-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	keyutils-devel
BuildRequires:	pkgconfig(dbus-1) >= 1.12.2
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	gtk-doc
%if !%{with bootstrap}
BuildRequires:	pkgconfig(libcryptsetup)
BuildRequires:	pkgconfig(python)
%endif
BuildRequires:	pkgconfig(libkmod) >= 5
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(libqrencode)
BuildRequires:	pkgconfig(libiptc)
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(blkid) >= 2.30
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(bash-completion)
%ifnarch %{armx} %{riscv}
BuildRequires:	valgrind-devel
BuildRequires:	gnu-efi >= 3.0.11
%endif
%ifnarch %{riscv}
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(polkit-gobject-1)
%endif
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libidn2)
#BuildRequires:	apparmor-devel
# To make sure _rundir is defined
BuildRequires:	rpm-build >= 2:4.14.0
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(mount) >= 2.27
# make sure we have /etc/os-release available, required by --with-distro
BuildRequires:	distro-release-common
%if !%{with bootstrap}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
# (tpg) this is needed to update /usr/share/systemd/kbd-model-map
BuildRequires:	kbd >= 2.2.0
%endif
Requires:	libcap-utils
Requires:	acl
Requires:	dbus >= 1.12.2
Requires(post):	coreutils >= 8.28
Requires(post):	grep
Requires:	basesystem-minimal
Requires:	util-linux >= 2.27
Requires:	shadow >= 2:4.5
Requires(post,postun):	setup >= 2.8.9
Requires:	kmod >= 24
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
Requires:	%{name}-macros = %{EVRD}
# (tpg) just to be sure we install this libraries
Requires:	%{libsystemd} = %{EVRD}
Requires:	%{libnss_myhostname} = %{EVRD}
Requires:	%{libnss_resolve} = %{EVRD}
Requires:	%{libnss_systemd} = %{EVRD}
Suggests:	%{name}-analyze
Suggests:	%{name}-boot
Suggests:	%{name}-console
Suggests:	%{name}-coredump
Suggests:	%{name}-documentation >= 236
Suggests:	%{name}-hwdb
Suggests:	%{name}-locale
Suggests:	%{name}-polkit
Suggests:	%{name}-cryptsetup
Suggests:	%{name}-bash-completion = %{EVRD}
#Suggests:	%{name}-zsh-completion = %{EVRD}

#(tpg)for future releases... systemd provides also a full functional syslog tool
Provides:	syslog-daemon
# (tpg) conflict with old sysvinit subpackage
%rename		systemd-sysvinit
Conflicts:	systemd-sysvinit < 207-1
# (eugeni) systemd should work as a drop-in replacement for sysvinit, but not obsolete it
Provides:	sysvinit = 2.87-23, SysVinit = 2.87-23
# (tpg) time to die
Obsoletes:	sysvinit < 2.87-23, SysVinit < 2.87-23
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
Obsoletes:	resolvconf < 1.75-6
Provides:	resolvconf = 1.75-6
Obsoletes:	bootchart < 2.0.11.4-3
Provides:	bootchart = 2.0.11.4-3
Obsoletes:	python-%{name} < 223
Provides:	python-%{name} = 223
Obsoletes:	gummiboot < 46
%rename		systemd-tools
%rename		systemd-units
%rename		udev
%if %{with compat32}
BuildRequires:	devel(libcap)
BuildRequires:	devel(libgcrypt)
BuildRequires:	devel(libip4tc)
BuildRequires:	devel(libip6tc)
BuildRequires:	devel(libpcre2-8)
BuildRequires:	devel(liblz4)
BuildRequires:	devel(libcrypto)
BuildRequires:	devel(libcurl)
BuildRequires:	devel(libcrypt) libcrypt-devel
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libidn2)
BuildRequires:	devel(libz)
BuildRequires:	devel(libdw)
BuildRequires:	devel(libdbus-1)
%endif

%description
systemd is a system and session manager for Linux, compatible with
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit.

%package boot
Summary:	EFI boot component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Conflicts:	%{name} < 245.20200426-3
Suggests:	%{name}-documentation = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description boot
Systemd boot tools to manage EFI boot.

%package console
Summary:	Console support for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
# need for /sbin/setfont etc
Requires:	kbd
Conflicts:	%{name} < 235-9
Suggests:	%{name}-documentation = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description console
Some systemd units and udev rules are useful only when
you have an actual console, this subpackage contains
these units.

%package networkd
Summary:	Network manager for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	networkmanager

%description networkd
A network manager for %{name}.

%{name}-networkd should not be used alongside NetworkManager
(which is the default in OpenMandriva).

Install and use with care.

%package coredump
Summary:	Coredump component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-documentation = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description coredump
Systemd coredump tools to manage coredumps and backtraces.

%package documentation
Summary:	Man pages and documentation for %{name}
Group:		Books/Computer books
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-locale = %{EVRD}
Obsoletes:	systemd-doc < 236-10
Conflicts:	systemd-doc < 236-10
%rename		udev-doc

%description documentation
Man pages and documentation for %{name}.

%package hwdb
Summary:	hwdb component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9
Conflicts:	%{name} < 238-4
Suggests:	%{name}-polkit = %{EVRD}
Suggests:	%{name}-documentation = %{EVRD}
Suggests:	%{name}-locale = %{EVRD}

%description hwdb
Hardware database management tool for %{name}.

%package locale
Summary:	Translations component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9

%description locale
Translations for %{name}.

%package polkit
Summary:	PolKit component for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 235-9

%description polkit
PolKit support for %{name}.

%package container
Summary:	Tools for containers and VMs
Group:		System/Base
Requires:	%{name} = %{EVRD}
Requires:	%{libnss_mymachines} = %{EVRD}
Conflicts:	%{name} < 235-1
Suggests:	%{name}-polkit = %{EVRD}
Suggests:	%{name}-bash-completion = %{EVRD}
Suggests:	%{name}-zsh-completion = %{EVRD}

%description container
Systemd tools to spawn and manage containers and virtual machines.
This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package analyze
Summary:	Tools for containers and VMs
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 238-4

%description analyze
Systemd tools to analyze and debug a running system:
systemd-analyze
systemd-cgls
systemd-cgtop
systemd-delta

%package journal-gateway
Summary:	Gateway for serving journal events over the network using HTTP
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{EVRD}
BuildRequires:	rpm-helper
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Obsoletes:	systemd < 206-7

%description journal-gateway
Offers journal events over the network using HTTP.

%if !%{with bootstrap}
%package cryptsetup
Summary:	Cryptsetup generators for %{name}
Group:		System/Base
Requires:	%{name} = %{EVRD}
Conflicts:	%{name} < 238-4

%description cryptsetup
Systemd generators for cryptsetup (Luks encryption and verity).
%endif

%package portable
Summary:	Tools for working with Portable Service Images
Group:		System/Base
Requires:	%{name} = %{EVRD}

%description portable
Portable service images contain an OS file system tree along with systemd
unit file information. A service image may be "attached" to the local
system.

If attached, a set of unit files are copied from the image to the host,
and extended with RootDirectory= or RootImage= assignments (in case of
service units) pointing to the image file or directory, ensuring the
services will run within the file system context of the image.

Portable service images are an efficient way to bundle multiple related
services and other units together, and transfer them as a whole between
systems. When these images are attached the local system the contained
units may run in most ways like regular system-provided units, either
with full privileges or inside strict sandboxing, depending on the
selected configuration.

%package -n %{libsystemd}
Summary:	Systemd library package
Group:		System/Libraries
# (tpg) old, pre 230 stuff - keep for smooth update from old relases
Provides:	libsystemd = 208-20
Obsoletes:	libsystemd < 208-20
Provides:	libsystemd-daemon = 208-20
Obsoletes:	libsystemd-daemon < 208-20
%rename		%{_lib}systemd-daemon0
Provides:	libsystemd-login = 208-20
Obsoletes:	libsystemd-login < 208-20
%rename		%{_lib}systemd-login0
Provides:	libsystemd-journal = 208-20
Obsoletes:	libsystemd-journal < 208-20
%rename		%{_lib}systemd-journal0
%rename		%{_lib}systemd-id1280
Obsoletes:	libsystemd-id1280 < 208-20
Provides:	libsystemd-id1280 = 208-20
%rename		%{_lib}systemd-id128_0

%description -n %{libsystemd}
This package provides the systemd shared library.

%package -n %{libsystemd_devel}
Summary:	Systemd library development files
Group:		Development/C
Requires:	%{name}-macros = %{EVRD}
Requires:	%{libsystemd} = %{EVRD}
# (tpg) old, pre 230 stuff - keep for smooth update from old relases
%rename		%{_lib}systemd-daemon0-devel
%rename		%{_lib}systemd-daemon-devel
%rename		%{_lib}systemd-login0-devel
%rename		%{_lib}systemd-login-devel
%rename		%{_lib}systemd-journal0-devel
%rename		%{_lib}systemd-journal-devel
%rename		%{_lib}systemd-id1280-devel
%rename		%{_lib}systemd-id128-devel

%description -n %{libsystemd_devel}
Development files for the systemd shared library.

%package -n %{libnss_myhostname}
Summary:	Library for local system host name resolution
Group:		System/Libraries
Provides:	libnss_myhostname = %{EVRD}
Provides:	nss_myhostname = %{EVRD}
# (tpg) fix update from 2014.0
Provides:	nss_myhostname = 208-20
Obsoletes:	nss_myhostname < 208-20

%description -n %{libnss_myhostname}
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%package -n %{libnss_mymachines}
Summary:	Provide hostname resolution for local container instances
Group:		System/Libraries
Provides:	libnss_mymachines = %{EVRD}
Provides:	nss_mymachines = %{EVRD}
Conflicts:	%{libnss_myhostname} < 235
Requires:	systemd-container = %{EVRD}

%description -n %{libnss_mymachines}
nss-mymachines is a plug-in module for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc), providing hostname resolution
for the names of containers running locally that are registered with 
systemd-machined.service(8). The container names are resolved to the IP 
addresses of the specific container, ordered by their scope. 
This functionality only applies to containers using network namespacing.

%package -n %{libnss_resolve}
Summary:	Provide hostname resolution via systemd-resolved.service
Group:		System/Libraries
Provides:	libnss_resolve = %{EVRD}
Provides:	nss_resolve= %{EVRD}
Requires:	%{name}-resolved = %{EVRD}
Conflicts:	%{libnss_myhostname} < 235

%description -n %{libnss_resolve}
nss-resolve is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc) enabling it to resolve host 
names via the systemd-resolved(8) local network name resolution service. 
It replaces the nss-dns plug-in module that traditionally resolves 
hostnames via DNS.

%package -n %{libnss_systemd}
Summary:	Provide UNIX user and group name resolution for dynamic users and groups
Group:		System/Libraries
Provides:	libnss_systemd = %{EVRD}
Provides:	nss_systemd = %{EVRD}
Conflicts:	%{libnss_myhostname} < 235

%description -n %{libnss_systemd}
nss-systemd is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc), providing UNIX user and 
group name resolution for dynamic users and groups allocated through 
the DynamicUser= option in systemd unit files. See systemd.exec(5) 
for details on this option.

%package -n %{libudev}
Summary:	Library for udev
Group:		System/Libraries
Obsoletes:	%{mklibname hal 1} <= 0.5.14-6

%description -n %{libudev}
Library for udev.

%package -n %{libudev_devel}
Summary:	Devel library for udev
Group:		Development/C
License:	LGPLv2+
Provides:	udev-devel = %{EVRD}
Requires:	%{libudev} = %{EVRD}
Requires:	%{name}-macros = %{EVRD}
Obsoletes:	%{_lib}udev0-devel < 236
Conflicts:	%{_lib}udev-devel < 236-8
Obsoletes:	%{_lib}udev-devel < 236-8

%description -n %{libudev_devel}
Devel library for udev.

%package zsh-completion
Summary:	zsh completions
Group:		Shells
Requires:	zsh

%description zsh-completion
This package contains zsh completion.

%package bash-completion
Summary:	bash completions
Group:		Shells
Requires:	bash

%description bash-completion
This package contains bash completion.

%package macros
Summary:	A RPM macros
Group:		Development/Other
Provides:	systemd-rpm-macros

%description macros
For building RPM packages to utilize standard systemd runtime macros.

%package resolved
Summary:	Network name resolution via D-Bus interface, NSS, and local DNS
Group:		System

%description resolved
systemd-resolved is a systemd service that provides network name resolution
to local applications via a D-Bus interface, the resolve NSS service,
and a local DNS stub listener

%if %{with compat32}
%package -n %{lib32systemd}
Summary:	Systemd library package (32-bit)
Group:		System/Libraries

%description -n %{lib32systemd}
This package provides the systemd shared library.

%package -n %{lib32systemd_devel}
Summary:	Systemd library development files (32-bit)
Group:		Development/C
Requires:	%{name}-macros = %{EVRD}
Requires:	%{lib32systemd} = %{EVRD}
Requires:	%{libsystemd_devel} = %{EVRD}

%description -n %{lib32systemd_devel}
Development files for the systemd shared library.

%package -n %{lib32nss_myhostname}
Summary:	Library for local system host name resolution (32-bit)
Group:		System/Libraries

%description -n %{lib32nss_myhostname}
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%package -n %{lib32nss_systemd}
Summary:	Provide UNIX user and group name resolution for dynamic users and groups (32-bit)
Group:		System/Libraries

%description -n %{lib32nss_systemd}
nss-systemd is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc), providing UNIX user and 
group name resolution for dynamic users and groups allocated through 
the DynamicUser= option in systemd unit files. See systemd.exec(5) 
for details on this option.

%package -n %{lib32udev}
Summary:	Library for udev (32-bit)
Group:		System/Libraries

%description -n %{lib32udev}
Library for udev.

%package -n %{lib32udev_devel}
Summary:	Devel library for udev (32-bit)
Group:		Development/C
License:	LGPLv2+
Requires:	%{libudev_devel} = %{EVRD}
Requires:	%{lib32udev} = %{EVRD}
Requires:	%{name}-macros = %{EVRD}

%description -n %{lib32udev_devel}
Devel library for udev.
%endif

%package oom
Summary:	Out of Memory handler
Group:		System/Base

%description oom
Out of Memory handler

%prep
%autosetup -p1

%build
%ifarch %{ix86}
mkdir -p bin
ln -sf %{_bindir}/ld.bfd bin/ld
PATH=$PWD/bin:$PATH
%endif

# FIXME
# Switch to
#	-Ddefault-hierarchy=unified \
# below once Docker has been fixed to work with it.
# In the mean time, hybrid provides cgroups2 features
# while keeping docker working.
# https://github.com/opencontainers/runc/issues/654
#
# In order to switch to cgroup2 it is enough to pass systemd.unified_cgroup_hierarchy=1 via kernel command line.
%serverbuild_hardened

%if %{with compat32}
%meson32 \
	-Dsplit-usr=true \
	-Dresolve=false \
	-Dhostnamed=false \
	-Dlocaled=false \
	-Dmachined=false \
	-Dportabled=false \
	-Duserdb=false \
	-Dhomed=false \
	-Dnetworkd=false \
	-Dtimedated=false \
	-Dtimesyncd=false \
	-Dselinux=false \
	-Dlibcryptsetup=false \
	-Dseccomp=false \
	-Dkmod=false \
	-Dpam=false \
	-Dqrencode=false \
	-Dp11kit=false \
	-Daudit=false \
	-Dmicrohttpd=false \
	-Dgnutls=false
%ninja_build -C build32
%endif

%if %{with gcc}
export CC=gcc
export CXX=g++
export LD=gcc
%endif
%meson \
	-Drootprefix="" \
	-Drootlibdir=/%{_lib} \
	-Dsysvinit-path=%{_initrddir} \
	-Dsysvrcnd-path=%{_sysconfdir}/rc.d \
	-Drc-local=/etc/rc.d/rc.local \
	-Defi=true \
	-Defi-libdir=%{_libdir} \
%ifnarch %{armx} %{riscv}
	-Dgnu-efi=true \
%endif
%if %{with bootstrap}
	-Dlibcryptsetup=false \
%else
	-Dlibcryptsetup=true \
%endif
	-Dsplit-usr=true \
	-Dsplit-bin=true \
	-Dxkbcommon=true \
	-Dtpm=true \
	-Ddev-kvm-mode=0666 \
	-Dkmod=true \
	-Dxkbcommon=true \
	-Dblkid=true \
%ifnarch %{riscv}
	-Dseccomp=true \
%else
	-Dseccomp=false \
%endif
	-Dima=true \
	-Dselinux=false \
	-Dapparmor=false \
	-Dpolkit=true \
	-Dxz=true \
	-Dzlib=true \
	-Dbzip2=false \
	-Dlz4=true \
	-Dpam=true \
	-Dacl=true \
	-Dsmack=true \
	-Dgcrypt=true \
	-Daudit=true \
	-Delfutils=true \
	-Dqrencode=true \
	-Dgnutls=true \
	-Dmicrohttpd=true \
	-Dlibidn2=true \
	-Dlibiptc=true \
	-Dlibcurl=true \
	-Dtpm=true \
	-Dhwdb=true \
	-Dsysusers=true \
	-Dman=true \
	-Dhtml=true \
	-Ddefault-kill-user-processes=false \
	-Dtests=unsafe \
	-Dinstall-tests=false \
%ifnarch %{ix86}
	-Db_lto=true \
%else
	-Db_lto=false \
%endif
	-Dloadkeys-path=/bin/loadkeys \
	-Dsetfont-path=/bin/setfont \
	-Dcertificate-root="%{_sysconfdir}/pki" \
	-Dfallback-hostname=openmandriva \
	-Dsupport-url="%{disturl}" \
	-Ddefault-hierarchy=hybrid \
	-Dtty-gid=5 \
	-Dusers-gid=100 \
	-Dnobody-user=nobody \
	-Dnobody-group=nogroup \
	-Dsystem-uid-max='999' \
	-Dsystem-gid-max='999' \
	-Dntp-servers='_gateway gateway 0.openmandriva.pool.ntp.org 1.openmandriva.pool.ntp.org 2.openmandriva.pool.ntp.org 3.openmandriva.pool.ntp.org' \
	-Ddns-servers='208.67.222.222 208.67.220.220'

%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
rm -rf %{buildroot}%{_sysconfdir} %{buildroot}/lib/{systemd,modprobe.d,udev}
# 32 bit cruft is not needed at early bootup...
mv %{buildroot}/lib/* %{buildroot}%{_prefix}/lib/
rmdir %{buildroot}/lib
%endif
%meson_install

mkdir -p %{buildroot}{/bin,%{_sbindir}}

# (bor) create late shutdown and sleep directory
mkdir -p %{buildroot}%{systemd_libdir}/system-shutdown
mkdir -p %{buildroot}%{systemd_libdir}/system-sleep

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/sbin
ln -s ..%{systemd_libdir}/%{name} %{buildroot}/bin/%{name}

# (tpg) install compat symlinks - enable when split-bin=true
for i in halt poweroff reboot; do
    ln -s /bin/systemctl %{buildroot}/bin/$i
done

ln -s /bin/loginctl %{buildroot}%{_bindir}/%{name}-loginctl

# (tpg) dracut needs this
ln -sf /bin/systemctl %{buildroot}%{_bindir}/systemctl
ln -sf /bin/systemd-escape %{buildroot}%{_bindir}/systemd-escape

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -rf %{buildroot}%{_sysconfdir}/%{name}/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/system/getty.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/dbus.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/syslog.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/halt.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/initrd-switch-root.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/initrd.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/kexec.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/poweroff.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/reboot.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/systemsound.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/system-update.target.wants
mkdir -p %{buildroot}/%{_prefix}/lib/%{name}/user/basic.target.wants
mkdir -p %{buildroot}/%{_prefix}/lib/%{name}/user/default.target.wants
mkdir -p %{buildroot}/%{_prefix}/lib/%{name}/user/sockets.target.wants

# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/%{name}/system/default.target

# (tpg) this is needed
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/system-generators
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/user-generators

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}/%{systemd_libdir}/system/bluetooth.target.wants

# (tpg) use systemd's own mounting capability
sed -i -e 's/^#MountAuto=yes$/MountAuto=yes/' %{buildroot}/etc/%{name}/system.conf
sed -i -e 's/^#SwapAuto=yes$/SwapAuto=yes/' %{buildroot}/etc/%{name}/system.conf

# (crazy) Do not do that .. is imposible to disable such services
# resolved will stay that way for other reasons and bugs we hit with 239/240  but after Lx4 is out
# it has to go from here too
# (tpg) explicitly enable these services
ln -sf /lib/%{name}/system/%{name}-resolved.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/%{name}-resolved.service

# (eugeni) install /run
mkdir %{buildroot}/run

# (tpg) create missing dir
mkdir -p %{buildroot}%{_libdir}/%{name}/user/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/user/default.target.wants

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

# (tpg) needed for containers
mkdir -p %{buildroot}%{_sysconfig}/%{name}/nspawn

# (cg) Set up the pager to make it generally more useful
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh << EOF
export SYSTEMD_PAGER="/usr/bin/less -FR"
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh

# Install logdir for journald
install -m 0755 -d %{buildroot}%{_logdir}/journal

#
install -m 0755 -d %{buildroot}%{_sysconfdir}/%{name}/network

# (tpg) Install default distribution preset policy for services
mkdir -p %{buildroot}%{systemd_libdir}/system-preset
# (tpg) add local user preset dir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/user-preset
# (tpg) add global user preset dir
mkdir -p %{buildroot}%{_prefix}/lib/%{name}/user-preset

# (tpg) install presets
install -m 0644 %{SOURCE12} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE13} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE14} %{buildroot}%{systemd_libdir}/system-preset/

# (tpg) install userspace presets
# (crazy) .. but not like this
#install -m 0644 %{SOURCE18} %{buildroot}%{_prefix}/lib/%{name}/user-preset/

# (tpg) remove 90-systemd-preset as it is included in ours 90-default.preset
rm -rf %{buildroot}%{systemd_libdir}/system-preset/90-systemd.preset

# Install rsyslog fragment
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/rsyslog.d/

# (tpg) silent kernel messages
# print only KERN_ERR and more serious alerts
echo "kernel.printk = 2 2 2 2" >> %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) by default enable SysRq
sed -i -e 's/^#kernel.sysrq = 0/kernel.sysrq = 1/' %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) use 100M as a default maximum value for journal logs
sed -i -e 's/^#SystemMaxUse=.*/SystemMaxUse=100M/' %{buildroot}%{_sysconfdir}/%{name}/journald.conf

%ifnarch %{armx} %{riscv}
install -m644 -D %{SOURCE21} %{buildroot}%{_datadir}/%{name}/bootctl/loader.conf
install -m644 -D %{SOURCE22} %{buildroot}%{_datadir}/%{name}/bootctl/omv.conf
%endif

# Install yum protection fragment
install -Dm0644 %{SOURCE24} %{buildroot}%{_sysconfdir}/dnf/protected.d/systemd.conf

# (tpg) update /usr/share/systemd/kbd-model-map based on kbd package
if [ -f /usr/share/systemd/kbd-model-map.generated ]; then
    cat /usr/share/systemd/kbd-model-map.generated >> %{buildroot}%{_datadir}/%{name}/kbd-model-map
fi
#################
#	UDEV	#
#	START	#
#################

install -m 644 %{SOURCE2} %{buildroot}%{udev_rules_dir}/
install -m 644 %{SOURCE3} %{buildroot}%{udev_rules_dir}/
mkdir -p  %{buildroot}%{_sysconfdir}/sysconfig/udev
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/udev/

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

ln -s ..%{systemd_libdir}/%{name}-udevd %{buildroot}/sbin/udevd
ln -s %{systemd_libdir}/%{name}-udevd %{buildroot}%{udev_libdir}/udevd

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

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{systemd_libdir}/system/systemd-udev-trigger.service.d/ %{SOURCE23}

# Pre-generate and pre-ship hwdb, to speed up first boot
./build/systemd-hwdb --root %{buildroot} --usr update || ./build/udevadm hwdb --root %{buildroot} --update --usr

# Compute catalog
./build/journalctl --root %{buildroot} --update-catalog

%find_lang %{name}

%include %{SOURCE1}

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 ] || [ $2 -ge 2 ]; then
    /bin/systemctl daemon-reexec 2>&1 || :
fi

%post
/bin/systemd-firstboot --setup-machine-id &>/dev/null ||:
/bin/systemd-sysusers &>/dev/null ||:
/bin/systemd-machine-id-setup &>/dev/null ||:
%{systemd_libdir}/systemd-random-seed save &>/dev/null ||:
/bin/systemctl daemon-reexec &>/dev/null ||:
/bin/journalctl --update-catalog &>/dev/null ||:
/bin/systemd-tmpfiles --create &>/dev/null ||:

# Init 90-default.preset
# never use preset-all
if [ $1 -eq 1 ] ; then
	# keep in sysnc with 90-default.preset
	/bin/systemctl preset remote-fs.target &>/dev/null ||:
	/bin/systemctl preset remote-cryptsetup.target &>/dev/null ||:
	/bin/systemctl preset machines.target &>/dev/null ||:
	/bin/systemctl preset getty@tty1.service &>/dev/null ||:
	/bin/systemctl preset systemd-bus-proxy.socket &>/dev/null ||:
	/bin/systemctl preset systemd-initctl.socket &>/dev/null ||:
	/bin/systemctl preset systemd-journald.socket &>/dev/null ||:
	/bin/systemctl preset systemd-timedated.service &>/dev/null ||:
	/bin/systemctl preset systemd-timesyncd.service &>/dev/null ||:
	/bin/systemctl preset systemd-rfkill.socket &>/dev/null ||:
	/bin/systemctl preset console-getty.service &>/dev/null ||:
	/bin/systemctl preset debug-shell.service &>/dev/null ||:
	/bin/systemctl preset halt.target &>/dev/null ||:
	/bin/systemctl preset kexec.target &>/dev/null ||:
	/bin/systemctl preset poweroff.target &>/dev/null ||:
	/bin/systemctl preset reboot.target &>/dev/null ||:
	/bin/systemctl preset rescue.target &>/dev/null ||:
	/bin/systemctl preset exit.target &>/dev/null ||:
	/bin/systemctl preset syslog.socket &>/dev/null ||:
fi

hostname_new=$(cat %{_sysconfdir}/hostname 2>/dev/null)
if [ -z "$hostname_new" ]; then
    hostname_old=$(cat /etc/sysconfig/network 2>/dev/null | grep HOSTNAME | cut -d "=" -f2)
    if [ ! -z "$hostname_old" ]; then
	printf '%s\n' "$hostname_old" >> %{_sysconfdir}/hostname
    else
	printf '%s\n' "localhost" >> %{_sysconfdir}/hostname
    fi
fi

%triggerin -- %{name} < 239
# (tpg) move sysctl.conf to /etc/sysctl.d as since 207 /etc/sysctl.conf is skipped
if [ -e %{_sysconfdir}/sysctl.conf ] && [ ! -L %{_sysconfdir}/sysctl.conf ]; then
	mv -f %{_sysconfdir}/sysctl.conf %{_sysconfdir}/sysctl.d/99-sysctl.conf
	ln -s %{_sysconfdir}/sysctl.d/99-sysctl.conf %{_sysconfdir}/sysctl.conf
fi

# Remove spurious /etc/fstab entries from very old installations
if [ -e /etc/fstab ]; then
	grep -v -E -q '^(devpts|tmpfs|sysfs|proc)' /etc/fstab || \
	    sed -i.rpm.bak -r '/^devpts\s+\/dev\/pts\s+devpts\s+defaults\s+/d; /^tmpfs\s+\/dev\/shm\s+tmpfs\s+defaults\s+/d; /^sysfs\s+\/sys\s+sysfs\s+defaults\s+/d; /^proc\s+\/proc\s+proc\s+defaults\s+/d' /etc/fstab || :
fi

# Try to read default runlevel from the old inittab if it exists
runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
if [ -z "$runlevel" ] ; then
	target="/lib/systemd/system/graphical.target"
    else
	target="/lib/systemd/system/runlevel$runlevel.target"
 fi

# And symlink what we found to the new-style default.target
/bin/ln -sf "$target" %{_sysconfdir}/systemd/system/default.target 2>&1 || :

%preun
if [ $1 -eq 0 ] ; then
    /bin/systemctl --quiet disable \
	    getty@tty1.service \
	    getty@getty.service \
	    remote-fs.target \
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
    /bin/systemctl daemon-reload > /dev/null 2>&1 || :
fi

%post hwdb
/bin/systemd-hwdb update >/dev/null 2>&1 || :

#triggerin -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
#ARG1=$1
#ARG2=$2
#shift
#shift
#
#units=${*#%{_unitdir}/}
#if [ $ARG1 -eq 1 -a $ARG2 -eq 1 ]; then
#    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
#    /bin/systemctl preset ${units} >/dev/null 2>&1 || :
#fi
#triggerun -- ^%{_unitdir}/.*\.(service|socket|path|timer)$
#ARG1=$1
#ARG2=$2
#shift
#shift

#skip="$(grep -l 'Alias=display-manager.service' $*)"
#units=${*#%{_unitdir}/}
#units=${units#${skip##*/}}
#if [ $ARG2 -eq 0 ]; then
#    /bin/systemctl --no-reload disable ${units} >/dev/null 2>&1 || :
#    /bin/systemctl stop ${units} >/dev/null 2>&1 || :
#fi

%triggerin -- %{libnss_myhostname} < 237
if [ -f /etc/nsswitch.conf ]; then
# sed-fu to add myhostanme to hosts line
	grep -v -E -q '^hosts:.* myhostname' /etc/nsswitch.conf &&
	sed -i.bak -e '
		/^hosts:/ !b
		/\<myhostname\>/ b
		s/[[:blank:]]*$/ myhostname/
		' /etc/nsswitch.conf &>/dev/null || :
fi

%triggerin -- %{libnss_mymachines} < 237
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^(passwd|group):.* mymachines' /etc/nsswitch.conf ||
	sed -i.bak -r -e '
		s/^(passwd|group):(.*)/\1: \2 mymachines/
		' /etc/nsswitch.conf &>/dev/null || :
fi

%triggerun -- %{libnss_mymachines} < 237
# sed-fu to remove mymachines from passwd and group lines of /etc/nsswitch.conf
# https://bugzilla.redhat.com/show_bug.cgi?id=1284325
# To avoid the removal, e.g. add a space at the end of the line.
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^(passwd|group):.* mymachines$' /etc/nsswitch.conf &&
	sed -i.bak -r -e '
		s/^(passwd:.*) mymachines$/\1/;
		s/^(group:.*) mymachines$/\1/;
		' /etc/nsswitch.conf &>/dev/null || :
fie

%triggerin -- %{libnss_resolve} < 237
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^hosts:.*resolve[[:space:]]*($|[[:alpha:]])' /etc/nsswitch.conf &&
	sed -i.bak -e '
		/^hosts:/ { s/resolve/& [!UNAVAIL=return]/}
		' /etc/nsswitch.conf &>/dev/null || :
fi

%triggerin -- %{libnss_systemd} < 237
if [ -f /etc/nsswitch.conf ]; then
	grep -E -q '^(passwd|group):.* systemd' /etc/nsswitch.conf ||
	sed -i.bak -r -e '
		s/^(passwd|group):(.*)/\1: \2 systemd/
		' /etc/nsswitch.conf &>/dev/null || :
fi

%pre journal-gateway
%_pre_groupadd systemd-journal-gateway systemd-journal-gateway
%_pre_useradd systemd-journal-gateway %{_var}/log/journal /sbin/nologin
%_pre_groupadd systemd-journal-remote systemd-journal-remote
%_pre_useradd systemd-journal-remote %{_var}/log/journal/remote /sbin/nologin
%_pre_groupadd systemd-journal-upload systemd-journal-upload
%_pre_useradd systemd-journal-upload %{_var}/log/journal/upload /sbin/nologin

%files
%dir /lib/firmware
%dir /lib/firmware/updates
%dir /lib/modprobe.d
%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%dir %{_datadir}/%{name}
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/catalog
%dir %{_prefix}/lib/%{name}/system-generators
%dir %{_prefix}/lib/%{name}/user
%dir %{_prefix}/lib/%{name}/user-preset
%dir %{_prefix}/lib/%{name}/user-generators
%dir %{_prefix}/lib/%{name}/user-environment-generators
%dir %{_prefix}/lib/%{name}/user/basic.target.wants
%dir %{_prefix}/lib/%{name}/user/default.target.wants
%dir %{_prefix}/lib/%{name}/user/sockets.target.wants
%dir %{_prefix}/lib/sysusers.d
%dir %{_prefix}/lib/tmpfiles.d
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/system
%dir %{_sysconfdir}/%{name}/system/getty.target.wants
%dir %{_sysconfdir}/%{name}/user
%dir %{_sysconfdir}/%{name}/user-preset
%dir %{_sysconfdir}/%{name}/user/default.target.wants
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/agents.d
%dir %{_sysconfdir}/udev/agents.d/usb
%dir %{_sysconfdir}/udev/rules.d
%dir %{systemd_libdir}
#dir %{systemd_libdir}/*-generators
%dir %{systemd_libdir}/system
%dir %{systemd_libdir}/system-preset
%dir %{systemd_libdir}/system-shutdown
%dir %{systemd_libdir}/system-sleep
%dir %{systemd_libdir}/system/systemd-udev-trigger.service.d
%dir %{systemd_libdir}/system/basic.target.wants
%dir %{systemd_libdir}/system/bluetooth.target.wants
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
%dir %{systemd_libdir}/system/halt.target.wants
%dir %{systemd_libdir}/system/initrd-switch-root.target.wants
%dir %{systemd_libdir}/system/initrd.target.wants
%dir %{systemd_libdir}/system/kexec.target.wants
%dir %{systemd_libdir}/system/poweroff.target.wants
%dir %{systemd_libdir}/system/reboot.target.wants
%dir %{systemd_libdir}/systemsound.target.wants
%dir %{systemd_libdir}/system/system-update.target.wants
%dir %{systemd_libdir}/system/timers.target.wants
%dir %{systemd_libdir}/system/machines.target.wants
%dir %{systemd_libdir}/system/remote-fs.target.wants
%dir %{systemd_libdir}/system/user-.slice.d
%dir %{udev_libdir}
%dir %{udev_libdir}/hwdb.d
%dir %{udev_rules_dir}
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
%ghost %config(noreplace,missingok) %attr(0644,root,root) %{_sysconfdir}/scsi_id.config
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timesync1.conf
%{_prefix}/lib/%{name}/user-generators/systemd-xdg-autostart-generator
/%{_lib}/security/pam_systemd.so
/bin/halt
/bin/journalctl
/bin/loginctl
/bin/poweroff
/bin/reboot
/bin/systemctl
/bin/%{name}
/bin/%{name}-ask-password
/bin/%{name}-escape
/bin/%{name}-firstboot
/bin/%{name}-inhibit
/bin/%{name}-machine-id-setup
/bin/%{name}-notify
/bin/%{name}-sysusers
/bin/%{name}-tmpfiles
/bin/%{name}-tty-ask-password-agent
/bin/udevadm
/bin/userdbctl
/sbin/init
/sbin/runlevel
/sbin/shutdown
/sbin/telinit
/sbin/halt
/sbin/poweroff
/sbin/reboot
%{_bindir}/busctl
%{_bindir}/hostnamectl
%{_bindir}/kernel-install
%{_bindir}/localectl
%{_bindir}/systemctl
%{_bindir}/systemd-cat
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-dissect
%{_bindir}/systemd-escape
%{_bindir}/systemd-id128
%{_bindir}/systemd-loginctl
%{_bindir}/systemd-mount
%{_bindir}/systemd-path
%{_bindir}/systemd-run
%{_bindir}/systemd-socket-activate
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-umount
%{_bindir}/timedatectl
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timesync1.service
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/%{name}/kbd-model-map
%{_datadir}/%{name}/language-fallback-map
%{_initrddir}/README
%{_logdir}/README
/lib/modprobe.d/systemd.conf
%{_prefix}/lib/kernel/install.d/*.install
%{_prefix}/lib/environment.d/99-environment.conf
%{_prefix}/lib/%{name}/user-preset/*.preset
%{_prefix}/lib/%{name}/user/*.service
%{_prefix}/lib/%{name}/user/*.target
%{_prefix}/lib/%{name}/user/*.timer
%{_prefix}/lib/%{name}/user/*.slice
%{_prefix}/lib/systemd/user-environment-generators/*
%{_prefix}/lib/tmpfiles.d/*.conf
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/xdg/%{name}
%dir %{systemd_libdir}/ntp-units.d
%{systemd_libdir}/ntp-units.d/80-systemd-timesync.list
%{_datadir}/factory/etc/issue
# Generators
%{systemd_libdir}/system-generators/systemd-bless-boot-generator
%{systemd_libdir}/system-generators/systemd-debug-generator
%{systemd_libdir}/system-generators/systemd-fstab-generator
%{systemd_libdir}/system-generators/systemd-getty-generator
%{systemd_libdir}/system-generators/systemd-gpt-auto-generator
%{systemd_libdir}/system-generators/systemd-hibernate-resume-generator
%{systemd_libdir}/system-generators/systemd-rc-local-generator
%{systemd_libdir}/system-generators/systemd-run-generator
%{systemd_libdir}/system-generators/systemd-system-update-generator
%{systemd_libdir}/system-generators/systemd-sysv-generator
# Presets
%{systemd_libdir}/system-preset/85-display-manager.preset
%{systemd_libdir}/system-preset/90-default.preset
%{systemd_libdir}/system-preset/99-default-disable.preset
# Mounts
%{systemd_libdir}/system/dev-hugepages.mount
%{systemd_libdir}/system/dev-mqueue.mount
%{systemd_libdir}/system/proc-sys-fs-binfmt_misc.automount
%{systemd_libdir}/system/proc-sys-fs-binfmt_misc.mount
%{systemd_libdir}/system/sys-fs-fuse-connections.mount
%{systemd_libdir}/system/sys-kernel-config.mount
%{systemd_libdir}/system/sys-kernel-debug.mount
%{systemd_libdir}/system/sys-kernel-tracing.mount
%{systemd_libdir}/system/tmp.mount
# Paths
%{systemd_libdir}/system/systemd-ask-password-console.path
%{systemd_libdir}/system/systemd-ask-password-wall.path
# Slices
%{systemd_libdir}/system/user.slice
# Services
%{systemd_libdir}/system/autovt@.service
%{systemd_libdir}/system/console-getty.service
%{systemd_libdir}/system/container-getty@.service
%{systemd_libdir}/system/dbus-org.freedesktop.hostname1.service
%{systemd_libdir}/system/dbus-org.freedesktop.locale1.service
%{systemd_libdir}/system/dbus-org.freedesktop.login1.service
%{systemd_libdir}/system/dbus-org.freedesktop.timedate1.service
%{systemd_libdir}/system/debug-shell.service
%{systemd_libdir}/system/emergency.service
%{systemd_libdir}/system/getty@.service
%{systemd_libdir}/system/initrd-cleanup.service
%{systemd_libdir}/system/initrd-parse-etc.service
%{systemd_libdir}/system/initrd-switch-root.service
%{systemd_libdir}/system/initrd-udevadm-cleanup-db.service
%{systemd_libdir}/system/kmod-static-nodes.service
%{systemd_libdir}/system/ldconfig.service
%{systemd_libdir}/system/modprobe@.service
%{systemd_libdir}/system/quotaon.service
%{systemd_libdir}/system/rc-local.service
%{systemd_libdir}/system/rescue.service
%{systemd_libdir}/system/system-update-cleanup.service
%{systemd_libdir}/system/systemd-ask-password-console.service
%{systemd_libdir}/system/systemd-ask-password-wall.service
%{systemd_libdir}/system/systemd-backlight@.service
%{systemd_libdir}/system/systemd-binfmt.service
%{systemd_libdir}/system/systemd-bless-boot.service
%{systemd_libdir}/system/systemd-boot-check-no-failures.service
%{systemd_libdir}/system/systemd-exit.service
%{systemd_libdir}/system/systemd-firstboot.service
%{systemd_libdir}/system/systemd-fsck-root.service
%{systemd_libdir}/system/systemd-fsck@.service
%{systemd_libdir}/system/systemd-halt.service
%{systemd_libdir}/system/systemd-hibernate-resume@.service
%{systemd_libdir}/system/systemd-hibernate.service
%{systemd_libdir}/system/systemd-hostnamed.service
%{systemd_libdir}/system/systemd-hybrid-sleep.service
%{systemd_libdir}/system/systemd-initctl.service
%{systemd_libdir}/system/systemd-journal-catalog-update.service
%{systemd_libdir}/system/systemd-journal-flush.service
%{systemd_libdir}/system/systemd-journald.service
%{systemd_libdir}/system/systemd-journald@.service
%{systemd_libdir}/system/systemd-kexec.service
%{systemd_libdir}/system/systemd-localed.service
%{systemd_libdir}/system/systemd-logind.service
%{systemd_libdir}/system/systemd-machine-id-commit.service
%{systemd_libdir}/system/systemd-modules-load.service
%{systemd_libdir}/system/systemd-poweroff.service
%{systemd_libdir}/system/systemd-pstore.service
%{systemd_libdir}/system/systemd-quotacheck.service
%{systemd_libdir}/system/systemd-random-seed.service
%{systemd_libdir}/system/systemd-reboot.service
%{systemd_libdir}/system/systemd-remount-fs.service
%{systemd_libdir}/system/systemd-rfkill.service
%{systemd_libdir}/system/systemd-suspend-then-hibernate.service
%{systemd_libdir}/system/systemd-suspend.service
%{systemd_libdir}/system/systemd-sysctl.service
%{systemd_libdir}/system/systemd-sysusers.service
%{systemd_libdir}/system/systemd-time-wait-sync.service
%{systemd_libdir}/system/systemd-timedated.service
%{systemd_libdir}/system/systemd-timesyncd.service
%{systemd_libdir}/system/systemd-tmpfiles-clean.service
%{systemd_libdir}/system/systemd-tmpfiles-setup-dev.service
%{systemd_libdir}/system/systemd-tmpfiles-setup.service
%{systemd_libdir}/system/systemd-udev-settle.service
%{systemd_libdir}/system/systemd-udev-trigger.service
%{systemd_libdir}/system/systemd-udevd.service
%{systemd_libdir}/system/systemd-update-done.service
%{systemd_libdir}/system/systemd-update-utmp-runlevel.service
%{systemd_libdir}/system/systemd-update-utmp.service
%{systemd_libdir}/system/systemd-user-sessions.service
%{systemd_libdir}/system/systemd-userdbd.service
%{systemd_libdir}/system/systemd-vconsole-setup.service
%{systemd_libdir}/system/systemd-volatile-root.service
%{systemd_libdir}/system/user-runtime-dir@.service
%{systemd_libdir}/system/user@.service
# Sockets
%{systemd_libdir}/system/syslog.socket
%{systemd_libdir}/system/systemd-initctl.socket
%{systemd_libdir}/system/systemd-journald-audit.socket
%{systemd_libdir}/system/systemd-journald-dev-log.socket
%{systemd_libdir}/system/systemd-journald-varlink@.socket
%{systemd_libdir}/system/systemd-journald.socket
%{systemd_libdir}/system/systemd-journald@.socket
%{systemd_libdir}/system/systemd-rfkill.socket
%{systemd_libdir}/system/systemd-udevd-control.socket
%{systemd_libdir}/system/systemd-udevd-kernel.socket
%{systemd_libdir}/system/systemd-userdbd.socket
# Targets
%{systemd_libdir}/system/basic.target
%{systemd_libdir}/system/blockdev@.target
%{systemd_libdir}/system/bluetooth.target
%{systemd_libdir}/system/boot-complete.target
%{systemd_libdir}/system/ctrl-alt-del.target
%{systemd_libdir}/system/default.target
%{systemd_libdir}/system/emergency.target
%{systemd_libdir}/system/exit.target
%{systemd_libdir}/system/final.target
%{systemd_libdir}/system/first-boot-complete.target
%{systemd_libdir}/system/getty-pre.target
%{systemd_libdir}/system/getty.target
%{systemd_libdir}/system/graphical.target
%{systemd_libdir}/system/halt.target
%{systemd_libdir}/system/hibernate.target
%{systemd_libdir}/system/hybrid-sleep.target
%{systemd_libdir}/system/initrd-fs.target
%{systemd_libdir}/system/initrd-root-device.target
%{systemd_libdir}/system/initrd-root-fs.target
%{systemd_libdir}/system/initrd-switch-root.target
%{systemd_libdir}/system/initrd.target
%{systemd_libdir}/system/kexec.target
%{systemd_libdir}/system/local-fs-pre.target
%{systemd_libdir}/system/local-fs.target
%{systemd_libdir}/system/multi-user.target
%{systemd_libdir}/system/network-online.target
%{systemd_libdir}/system/network-pre.target
%{systemd_libdir}/system/network.target
%{systemd_libdir}/system/nss-lookup.target
%{systemd_libdir}/system/nss-user-lookup.target
%{systemd_libdir}/system/paths.target
%{systemd_libdir}/system/poweroff.target
%{systemd_libdir}/system/printer.target
%{systemd_libdir}/system/reboot.target
%{systemd_libdir}/system/remote-fs-pre.target
%{systemd_libdir}/system/remote-fs.target
%{systemd_libdir}/system/rescue.target
%{systemd_libdir}/system/rpcbind.target
%{systemd_libdir}/system/runlevel0.target
%{systemd_libdir}/system/runlevel1.target
%{systemd_libdir}/system/runlevel2.target
%{systemd_libdir}/system/runlevel3.target
%{systemd_libdir}/system/runlevel4.target
%{systemd_libdir}/system/runlevel5.target
%{systemd_libdir}/system/runlevel6.target
%{systemd_libdir}/system/shutdown.target
%{systemd_libdir}/system/sigpwr.target
%{systemd_libdir}/system/sleep.target
%{systemd_libdir}/system/slices.target
%{systemd_libdir}/system/smartcard.target
%{systemd_libdir}/system/sockets.target
%{systemd_libdir}/system/sound.target
%{systemd_libdir}/system/suspend-then-hibernate.target
%{systemd_libdir}/system/suspend.target
%{systemd_libdir}/system/swap.target
%{systemd_libdir}/system/sysinit.target
%{systemd_libdir}/system/system-update-pre.target
%{systemd_libdir}/system/system-update.target
%{systemd_libdir}/system/time-set.target
%{systemd_libdir}/system/time-sync.target
%{systemd_libdir}/system/timers.target
%{systemd_libdir}/system/umount.target
# Timers
%{systemd_libdir}/system/systemd-tmpfiles-clean.timer
# Udev...
%{systemd_libdir}/system/systemd-udev-trigger.service.d/systemd-udev-trigger-no-reload.conf
%{systemd_libdir}/system/graphical.target.wants/systemd-update-utmp-runlevel.service
%{systemd_libdir}/system/local-fs.target.wants/tmp.mount
%{systemd_libdir}/system/multi-user.target.wants/systemd-ask-password-wall.path
%{systemd_libdir}/system/multi-user.target.wants/systemd-logind.service
%{systemd_libdir}/system/multi-user.target.wants/systemd-update-utmp-runlevel.service
%{systemd_libdir}/system/multi-user.target.wants/systemd-user-sessions.service
%{systemd_libdir}/system/multi-user.target.wants/getty.target
%{systemd_libdir}/system/rescue.target.wants/systemd-update-utmp-runlevel.service
%{systemd_libdir}/system/sockets.target.wants/systemd-initctl.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-journald-audit.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-journald-dev-log.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-journald.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-udevd-control.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-udevd-kernel.socket
%{systemd_libdir}/system/sysinit.target.wants/dev-hugepages.mount
%{systemd_libdir}/system/sysinit.target.wants/dev-mqueue.mount
%{systemd_libdir}/system/sysinit.target.wants/kmod-static-nodes.service
%{systemd_libdir}/system/sysinit.target.wants/ldconfig.service
%{systemd_libdir}/system/sysinit.target.wants/proc-sys-fs-binfmt_misc.automount
%{systemd_libdir}/system/sysinit.target.wants/sys-fs-fuse-connections.mount
%{systemd_libdir}/system/sysinit.target.wants/sys-kernel-config.mount
%{systemd_libdir}/system/sysinit.target.wants/sys-kernel-debug.mount
%{systemd_libdir}/system/sysinit.target.wants/sys-kernel-tracing.mount
%{systemd_libdir}/system/sysinit.target.wants/systemd-ask-password-console.path
%{systemd_libdir}/system/sysinit.target.wants/systemd-binfmt.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-firstboot.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-journal-catalog-update.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-journal-flush.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-journald.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-machine-id-commit.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-modules-load.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-random-seed.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-sysctl.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-sysusers.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-tmpfiles-setup-dev.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-tmpfiles-setup.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-udev-trigger.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-udevd.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-update-done.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-update-utmp.service
%{systemd_libdir}/system/user-.slice.d/10-defaults.conf
%{systemd_libdir}/system/usb-gadget.target
%{systemd_libdir}/system/timers.target.wants/systemd-tmpfiles-clean.timer
%{systemd_libdir}/systemd
%{systemd_libdir}/systemd-ac-power
%{systemd_libdir}/systemd-backlight
%{systemd_libdir}/systemd-binfmt
%{systemd_libdir}/systemd-bless-boot
%{systemd_libdir}/systemd-boot-check-no-failures
%{systemd_libdir}/systemd-cgroups-agent
%{systemd_libdir}/systemd-export
%{systemd_libdir}/systemd-fsck
%{systemd_libdir}/systemd-growfs
%{systemd_libdir}/systemd-hibernate-resume
%{systemd_libdir}/systemd-hostnamed
%{systemd_libdir}/systemd-import-fs
%{systemd_libdir}/systemd-initctl
%{systemd_libdir}/systemd-journald
%{systemd_libdir}/systemd-localed
%{systemd_libdir}/systemd-logind
%{systemd_libdir}/systemd-makefs
%{systemd_libdir}/systemd-modules-load
%{systemd_libdir}/systemd-pstore
%{systemd_libdir}/systemd-quotacheck
%{systemd_libdir}/systemd-random-seed
%{systemd_libdir}/systemd-remount-fs
%{systemd_libdir}/systemd-reply-password
%{systemd_libdir}/systemd-rfkill
%{systemd_libdir}/systemd-shutdown
%{systemd_libdir}/systemd-sleep
%{systemd_libdir}/systemd-socket-proxyd
%{systemd_libdir}/systemd-sulogin-shell
%{systemd_libdir}/systemd-sysctl
%{systemd_libdir}/systemd-time-wait-sync
%{systemd_libdir}/systemd-timedated
%{systemd_libdir}/systemd-timesyncd
%{systemd_libdir}/systemd-udevd
%{systemd_libdir}/systemd-update-done
%{systemd_libdir}/systemd-update-utmp
%{systemd_libdir}/systemd-user-runtime-dir
%{systemd_libdir}/systemd-user-sessions
%{systemd_libdir}/systemd-userdbd
%{systemd_libdir}/systemd-userwork
%{systemd_libdir}/systemd-veritysetup
%{systemd_libdir}/systemd-volatile-root
%{systemd_libdir}/systemd-xdg-autostart-condition
# (tpg) internal library - only systemd uses it
%{systemd_libdir}/libsystemd-shared-%{major}.so
#
%{udev_rules_dir}/10-imx.rules
%{udev_rules_dir}/50-udev-default.rules
%{udev_rules_dir}/50-udev-mandriva.rules
%{udev_rules_dir}/60-autosuspend.rules
%{udev_rules_dir}/60-block.rules
%{udev_rules_dir}/60-fido-id.rules
%{udev_rules_dir}/60-persistent-storage.rules
%{udev_rules_dir}/60-sensor.rules
%{udev_rules_dir}/60-serial.rules
%{udev_rules_dir}/64-btrfs.rules
%{udev_rules_dir}/69-printeracl.rules
%{udev_rules_dir}/70-power-switch.rules
%{udev_rules_dir}/70-uaccess.rules
%{udev_rules_dir}/71-seat.rules
%{udev_rules_dir}/73-seat-late.rules
%{udev_rules_dir}/75-net-description.rules
%{udev_rules_dir}/80-drivers.rules
%{udev_rules_dir}/80-net-setup-link.rules
%{udev_rules_dir}/99-systemd.rules
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal
/sbin/udevadm
/sbin/udevd
%{_bindir}/udevadm
%{_sbindir}/udevadm
%attr(0755,root,root) %{udev_libdir}/ata_id
%attr(0755,root,root) %{udev_libdir}/fido_id
%attr(0755,root,root) %{udev_libdir}/scsi_id
%{udev_libdir}/udevd
%config(noreplace) %{_prefix}/lib/sysctl.d/50-default.conf
# This file exists only on 64-bit arches
%ifnarch %{ix86} %{arm}
%config(noreplace) %{_prefix}/lib/sysctl.d/50-pid-max.conf
%endif
%config(noreplace) %{_prefix}/lib/sysusers.d/basic.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-remote.conf
%config(noreplace) %{_prefix}/lib/pam.d/systemd-user
%config(noreplace) %{_sysconfdir}/rsyslog.d/listen.conf
%config(noreplace) %{_sysconfdir}/sysconfig/udev
%config(noreplace) %{_sysconfdir}/%{name}/journald.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
%config(noreplace) %{_sysconfdir}/%{name}/logind.conf
%config(noreplace) %{_sysconfdir}/%{name}/pstore.conf
%config(noreplace) %{_sysconfdir}/%{name}/sleep.conf
%config(noreplace) %{_sysconfdir}/%{name}/system.conf
%config(noreplace) %{_sysconfdir}/%{name}/timesyncd.conf
%config(noreplace) %{_sysconfdir}/%{name}/user.conf
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%config(noreplace) %{_sysconfdir}/dnf/protected.d/systemd.conf
%{_localstatedir}/lib/systemd/catalog/database
# This takes care of interface renaming etc. -- it is NOT for networkd
%dir %{systemd_libdir}/network
%{systemd_libdir}/network/99-default.link

%files portable
%dir %{systemd_libdir}/portable
%{_datadir}/dbus-1/system.d/org.freedesktop.portable1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.portable1.service
%{systemd_libdir}/portable/*
%{systemd_libdir}/system/dbus-org.freedesktop.portable1.service
%{systemd_libdir}/system/systemd-portabled.service
%{systemd_libdir}/systemd-portabled
%{_datadir}/polkit-1/actions/org.freedesktop.portable1.policy
%{_prefix}/lib/tmpfiles.d/portables.conf
/bin/portablectl

%files journal-gateway
%config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/%{name}-remote.conf
%dir %{_datadir}/%{name}/gatewayd
%{systemd_libdir}/%{name}-journal-gatewayd
%{systemd_libdir}/%{name}-journal-remote
%{systemd_libdir}/%{name}-journal-upload
%{systemd_libdir}/system/%{name}-journal-gatewayd.service
%{systemd_libdir}/system/%{name}-journal-gatewayd.socket
%{systemd_libdir}/system/%{name}-journal-remote.service
%{systemd_libdir}/system/%{name}-journal-remote.socket
%{systemd_libdir}/system/%{name}-journal-upload.service
%{_datadir}/%{name}/gatewayd/browse.html

%files container
%{systemd_libdir}/system/dbus-org.freedesktop.import1.service
%{systemd_libdir}/system/dbus-org.freedesktop.machine1.service
%{systemd_libdir}/system/machine.slice
%{systemd_libdir}/system/machines.target
%{systemd_libdir}/system/machines.target.wants/var-lib-machines.mount
%{systemd_libdir}/system/remote-fs.target.wants/var-lib-machines.mount
%{systemd_libdir}/system/systemd-importd.service
%{systemd_libdir}/system/systemd-machined.service
%{systemd_libdir}/system/systemd-nspawn@.service
%{systemd_libdir}/system/var-lib-machines.mount
%{systemd_libdir}/systemd-import
%{systemd_libdir}/systemd-importd
%{systemd_libdir}/systemd-machined
%{systemd_libdir}/systemd-pull
%{systemd_libdir}/import-pubring.gpg
%dir %{_sysconfig}/%{name}/nspawn
/bin/machinectl
%{_bindir}/systemd-nspawn
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.import1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.import1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy

%files -n %{libnss_mymachines}
/%{_lib}/libnss_mymachines.so.%{libnss_major}

%files -n %{libnss_myhostname}
/%{_lib}/libnss_myhostname.so.%{libnss_major}*

%files -n %{libnss_resolve}
/%{_lib}/libnss_resolve.so.%{libnss_major}

%files -n %{libnss_systemd}
/%{_lib}/libnss_systemd.so.%{libnss_major}

%files -n %{libsystemd}
/%{_lib}/libsystemd.so.%{libsystemd_major}*

%files -n %{libsystemd_devel}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/_sd-common.h
%{_includedir}/%{name}/sd-bus-protocol.h
%{_includedir}/%{name}/sd-bus-vtable.h
%{_includedir}/%{name}/sd-bus.h
%{_includedir}/%{name}/sd-device.h
%{_includedir}/%{name}/sd-event.h
%{_includedir}/%{name}/sd-hwdb.h
%{_includedir}/%{name}/sd-id128.h
%{_includedir}/%{name}/sd-journal.h
%{_includedir}/%{name}/sd-login.h
%{_includedir}/%{name}/sd-messages.h
%{_includedir}/%{name}/sd-daemon.h
%{_includedir}/%{name}/sd-path.h
/%{_lib}/lib%{name}.so
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/lib%{name}.pc

%files -n %{libudev}
/%{_lib}/libudev.so.%{udev_major}*

%files -n %{libudev_devel}
/%{_lib}/libudev.so
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/udev.pc
%{_includedir}/libudev.h

%files analyze
%{_bindir}/%{name}-analyze
%{_bindir}/%{name}-cgls
%{_bindir}/%{name}-cgtop
%{_bindir}/%{name}-delta

%files boot
%{_bindir}/bootctl
%{systemd_libdir}/system/systemd-boot-system-token.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-boot-system-token.service
%ifnarch %{armx} %{riscv}
%dir %{_prefix}/lib/%{name}/boot
%dir %{_prefix}/lib/%{name}/boot/efi
%dir %{_datadir}/%{name}/bootctl
%{_prefix}/lib/%{name}/boot/efi/*.efi
%{_prefix}/lib/%{name}/boot/efi/*.stub
%{_datadir}/%{name}/bootctl/*.conf
%endif

%files console
%{systemd_libdir}/systemd-vconsole-setup
%{systemd_libdir}/system/serial-getty@.service
%{udev_rules_dir}/90-vconsole.rules
%{udev_rules_dir}/70-mouse.rules
%{udev_rules_dir}/60-drm.rules
%{udev_rules_dir}/60-persistent-input.rules
%{udev_rules_dir}/70-touchpad.rules
%{udev_rules_dir}/60-evdev.rules
%{udev_rules_dir}/60-input-id.rules

%files coredump
%config(noreplace) %{_sysconfdir}/%{name}/coredump.conf
%{_bindir}/coredumpctl
%{_prefix}/lib/sysctl.d/50-coredump.conf
%{systemd_libdir}/systemd-coredump
%{systemd_libdir}/system/systemd-coredump.socket
%{systemd_libdir}/system/systemd-coredump@.service
%{systemd_libdir}/system/sockets.target.wants/systemd-coredump.socket

%files documentation
%doc %{_docdir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8.*

%files hwdb
%ghost %{_sysconfdir}/udev/hwdb.bin
%{systemd_libdir}/system/sysinit.target.wants/systemd-hwdb-update.service
%{systemd_libdir}/system/systemd-hwdb-update.service
/bin/systemd-hwdb
%{udev_libdir}/*.bin
%{udev_libdir}/hwdb.d/*.hwdb
%{udev_rules_dir}/60-cdrom_id.rules
%{udev_rules_dir}/60-persistent-alsa.rules
%{udev_rules_dir}/60-persistent-storage-tape.rules
%{udev_rules_dir}/60-persistent-v4l.rules
%{udev_rules_dir}/70-joystick.rules
%{udev_rules_dir}/75-probe_mtd.rules
%{udev_rules_dir}/78-sound-card.rules
%{udev_libdir}/cdrom_id
%{udev_libdir}/mtd_probe
%{udev_libdir}/v4l_id

%files locale -f %{name}.lang
%{_prefix}/lib/%{name}/catalog/*.catalog

%files polkit
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy

%files networkd
%{_sysconfdir}/systemd/networkd.conf
%dir %{_sysconfdir}/%{name}/network
%{systemd_libdir}/system/systemd-network-generator.service
%{systemd_libdir}/system/systemd-networkd-wait-online.service
%{systemd_libdir}/system/systemd-networkd.service
%{systemd_libdir}/system/systemd-networkd.socket
%{systemd_libdir}/systemd-network-generator
%{systemd_libdir}/systemd-networkd
%{systemd_libdir}/systemd-networkd-wait-online
%{_datadir}/dbus-1/system.d/org.freedesktop.network1.conf
/bin/networkctl
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%{systemd_libdir}/network/80-container-host0.network
%{systemd_libdir}/network/80-container-ve.network
%{systemd_libdir}/network/80-container-vz.network
%{systemd_libdir}/network/80-vm-vt.network
%{systemd_libdir}/network/80-wifi-adhoc.network
%{systemd_libdir}/network/80-wifi-ap.network.example
%{systemd_libdir}/network/80-wifi-station.network.example
%{_datadir}/polkit-1/actions/org.freedesktop.network1.policy
%{_datadir}/polkit-1/rules.d/systemd-networkd.rules

%files resolved
/sbin/resolvconf
%{_datadir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%{_bindir}/systemd-resolve
%{_bindir}/resolvectl
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{systemd_libdir}/resolv.conf
%{systemd_libdir}/system/systemd-resolved.service
%{systemd_libdir}/system/multi-user.target.wants/systemd-resolved.service
%{systemd_libdir}/systemd-resolved
%config(noreplace) %{_sysconfdir}/%{name}/resolved.conf
%{_datadir}/polkit-1/actions/org.freedesktop.resolve1.policy

%post resolved
# (tpg) create resolv.conf based on systemd
if [ $1 -eq 1 ]; then
    /bin/systemctl preset systemd-resolved.service &>/dev/null ||:
# (tpg) link to resolv.conf from systemd
    if [ -e /etc/resolv.conf ]; then
	rm -f /etc/resolv.conf
    fi
    ln -sf ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
fi

if [ $1 -ge 1 ]; then
    if [ ! -e /run/systemd/resolve/resolv.conf ] || [ ! -e /run/systemd/resolve/stub-resolv.conf ]; then
	mkdir -p /run/systemd/resolve
	printf '%s\n' "nameserver 208.67.222.222" "nameserver 208.67.220.220" > /run/systemd/resolve/resolv.conf
	printf '%s\n' "nameserver 208.67.222.222" "nameserver 208.67.220.220" > /run/systemd/resolve/stub-resolv.conf
    fi
fi

if [ $1 -ge 2 ]; then
    /bin/systemctl restart systemd-resolved.service 2>&1 || :
fi

%preun networkd
if [ $1 -eq 0 ] ; then
    /bin/systemctl --quiet disable systemd-networkd.service 2>&1 || :
fi

%if !%{with bootstrap}
%files cryptsetup
%{systemd_libdir}/systemd-cryptsetup
%{systemd_libdir}/system-generators/systemd-cryptsetup-generator
%{systemd_libdir}/system-generators/systemd-veritysetup-generator
%{systemd_libdir}/system/sysinit.target.wants/cryptsetup.target
%{systemd_libdir}/system/system-systemd\x2dcryptsetup.slice
%{systemd_libdir}/system/remote-cryptsetup.target
%{systemd_libdir}/system/cryptsetup-pre.target
%{systemd_libdir}/system/cryptsetup.target
%{systemd_libdir}/system/initrd-root-device.target.wants/remote-cryptsetup.target
%endif

%files zsh-completion
%{_datadir}/zsh/site-functions/*

%files bash-completion
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/*

%files macros
%{_rpmmacrodir}/macros.systemd

%files oom
/bin/oomctl
%{_sysconfdir}/systemd/oomd.conf
/lib/systemd/system/systemd-oomd.service
/lib/systemd/systemd-oomd
%{_datadir}/dbus-1/system-services/org.freedesktop.oom1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.oom1.conf

%if %{with compat32}
%files -n %{lib32nss_myhostname}
%{_prefix}/lib/libnss_myhostname.so.*

%files -n %{lib32nss_systemd}
%{_prefix}/lib/libnss_systemd.so.*

%files -n %{lib32systemd}
%{_prefix}/lib/libsystemd.so.*

%files -n %{lib32udev}
%{_prefix}/lib/libudev.so.*

%files -n %{lib32systemd_devel}
%{_prefix}/lib/libsystemd.so
%{_prefix}/lib/pkgconfig/libsystemd.pc

%files -n %{lib32udev_devel}
%{_prefix}/lib/libudev.so
%{_prefix}/lib/pkgconfig/libudev.pc
%endif
