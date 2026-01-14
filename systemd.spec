# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# -fstack-protector-all causes the check for -static-pie to fail
# (undefined references to __stack_chk_fail
%undefine _ssp_cflags
%undefine _fortify_cflags

# (tpg) optimize it a bit
%global optflags %{optflags} -O2 -Wno-implicit-int

%bcond_with bootstrap
%ifarch %{efi}
%bcond_without bootloader
%else
%bcond_with bootloader
%endif

# (tpg) do not reqire pkg-config
%global __requires_exclude pkg-config

%define libsystemd_major 0
%define libnss_major 2

%define libsystemd %mklibname %{name}
%define libsystemd_devel %mklibname %{name} -d
%define lib32systemd lib%{name}
%define lib32systemd_devel lib%{name}-devel

%define libnss_myhostname %mklibname nss_myhostname
%define libnss_mymachines %mklibname nss_mymachines
%define libnss_resolve %mklibname nss_resolve
%define libnss_systemd %mklibname nss_systemd
%define lib32nss_myhostname libnss_myhostname
%define lib32nss_systemd libnss_systemd

%define udev_major 1
%define libudev %mklibname udev
%define libudev_devel %mklibname udev -d
%define lib32udev libudev
%define lib32udev_devel libudev-devel

%define systemd_libdir %{_prefix}/lib/systemd
%define udev_libdir %{_prefix}/lib/udev
%define udev_rules_dir %{udev_libdir}/rules.d
%define udev_user_rules_dir %{_sysconfdir}/udev/rules.d

%define major %(echo %{version} |cut -d. -f1)
%define stable %(if echo %{version} |grep -q \\.; then echo %{version} |cut -d. -f2; else echo 0; fi)

%define oldlibsystemd %mklibname %{name} 0
%define oldlib32systemd lib%{name}0
%define oldlibnss_myhostname %mklibname nss_myhostname 2
%define oldlibnss_mymachines %mklibname nss_mymachines 2
%define oldlibnss_resolve %mklibname nss_resolve 2
%define oldlibnss_systemd %mklibname nss_systemd 2
%define oldlib32nss_myhostname libnss_myhostname2
%define oldlib32nss_systemd libnss_systemd2
%define oldlibudev %mklibname udev 1
%define oldlib32udev libudev1

Summary:	A System and Session Manager
Name:		systemd
Version:	259
Source0:	https://github.com/systemd/systemd/archive/refs/tags/v%{version}.tar.gz
Release:	1
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		https://systemd.io/
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
Source18:	90-user-default.preset
Source19:	10-imx.rules
Source20:	20-wired.network
# (tpg) EFI bootctl
Source21:	efi-loader.conf
Source22:	efi-omv.conf

Source23:	systemd-udev-trigger-no-reload.conf
# (tpg) protect systemd from unistnalling it
Source24:	yum-protect-systemd.conf

Source25:	systemd-remote.sysusers

Source26:	10-oomd-defaults.conf
Source27:	10-oomd-per-slice-defaults.conf
Source28:	10-timeout-abort.conf

### OMV patches###
Patch1:		systemd-254-efi-cflags.patch
# disable coldplug for storage and device pci (nokmsboot/failsafe boot option required for proprietary video driver handling)
Patch2:		0503-Disable-modprobe-pci-devices-on-coldplug-for-storage.patch
Patch3:		0511-login-mark-nokmsboot-fb-devices-as-master-of-seat.patch 
Patch5:		systemd-216-set-udev_log-to-err.patch
Patch8:		systemd-206-set-max-journal-size-to-150M.patch
Patch9:		systemd-245-disable-audit-by-default.patch
Patch11:	systemd-220-silent-fsck-on-boot.patch
Patch14:	systemd-217-do-not-run-systemd-firstboot-in-containers.patch
Patch15:	0500-create-default-links-for-primary-cd_dvd-drive.patch
Patch17:	0515-Add-path-to-locale-search.patch
Patch18:	0516-udev-silence-version-print.patch
Patch19:	systemd-243-random-seed-no-insane-timeouts.patch

# (tpg) ClearLinux patches
Patch100:	0001-journal-raise-compression-threshold.patch
#Patch101:	0002-journal-Add-option-to-skip-boot-kmsg-events.patch
Patch102:	0003-core-use-mmap-to-load-files.patch
#Patch103:	0005-journal-flush-var-kmsg-after-starting-disable-kmsg-f.patch
Patch104:	0007-sd-event-return-malloc-memory-reserves-when-main-loo.patch
Patch107:	0016-tmpfiles-Make-var-cache-ldconfig-world-readable.patch
Patch108:	0018-more-udev-children-workers.patch
Patch110:	0023-DHCP-retry-faster.patch
Patch111:	0024-Remove-libm-memory-overhead.patch
Patch112:	0025-skip-not-present-ACPI-devices.patch
Patch113:	0027-Make-timesyncd-a-simple-service.patch
Patch116:	0031-Don-t-do-transient-hostnames-we-set-ours-already.patch
Patch117:	0032-don-t-use-libm-just-for-integer-exp10.patch
#Patch119:	0033-Notify-systemd-earlier-that-resolved-is-ready.patch
#Patch120:	0038-Localize-1-symbol.patch

# (tpg) OMV patches
# (tpg) needed for 0038-Localize-1-symbol.patch
Patch1003:	systemd-250-compile.patch

# (tpg) Fedora patches
Patch1100:	https://src.fedoraproject.org/rpms/systemd/raw/rawhide/f/use-bfq-scheduler.patch

# Upstream patches from master that haven't landed in -stable yet

BuildRequires:	meson
BuildRequires:	quota
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
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(passwdqc)
BuildRequires:	gtk-doc
BuildRequires:	rsync
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
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(blkid) >= 2.30
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(libbpf)
BuildRequires:	bpftool
BuildRequires:	atomic-devel
BuildRequires:	efi-srpm-macros
%ifnarch %{armx} %{riscv}
BuildRequires:	valgrind-devel
%endif
%ifarch %{efi}
BuildRequires:	python%{pyver}dist(pyelftools)
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
BuildRequires:	rpm-build >= 4.14.0
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(mount) >= 2.27
BuildRequires:	pkgconfig(fdisk)
BuildRequires:	pkgconfig(pwquality)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	python%{pyver}dist(jinja2)
BuildRequires:	python%{pyver}dist(pefile)
BuildRequires:	pkgconfig(tss2-sys)
# make sure we have /etc/os-release available, required by --with-distro
BuildRequires:	distro-release-OpenMandriva
%if !%{with bootstrap}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
# (tpg) this is needed to update /usr/share/systemd/kbd-model-map
BuildRequires:	kbd >= 2.2.0
%endif
Requires:	libcap-utils
Requires:	acl
Requires(meta):	dbus >= 1.12.2
Requires(post):	coreutils >= 8.28
Requires(post):	grep
Requires:	(util-linux-core or util-linux)
Recommends:	kmod >= 24
Conflicts:	initscripts < 9.24
Requires:	udev = %{EVRD}
Provides:	should-restart = system
Requires(meta):	(%{name}-rpm-macros = %{EVRD} if rpm-build)
# (tpg) just to be sure we install this libraries
Requires:	%{libsystemd} = %{EVRD}
Requires:	%{libnss_myhostname} = %{EVRD}
Recommends:	%{name}-resolved = %{EVRD}
Recommends:	%{libnss_resolve} = %{EVRD}
Requires:	%{libnss_systemd} = %{EVRD}
Suggests:	%{name}-analyze
%ifarch %{efi}
Recommends:	%{name}-boot
%endif
Recommends:	%{name}-console
Suggests:	%{name}-coredump
Suggests:	%{name}-documentation >= 236
Suggests:	%{name}-hwdb
Suggests:	%{name}-locale
Suggests:	%{name}-polkit
Suggests:	%{name}-bash-completion
%if ! %{with bootstrap}
Suggests:	%{name}-cryptsetup
%endif

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
# (tpg) moved form makedev package
Provides:	dev
# FIXME
Obsoletes:	python-%{name} < 223
Provides:	python-%{name} = 223
# Older dracut fails to include systemd-executor
Conflicts:	dracut < 059-5
%if %{with compat32}
BuildRequires:	libc6
BuildRequires:	devel(libcap)
BuildRequires:	devel(libpcre2-8)
BuildRequires:	devel(libcrypto)
BuildRequires:	devel(libcrypt) libcrypt-devel
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libzstd)
BuildRequires:	devel(libidn2)
BuildRequires:	devel(libz)
BuildRequires:	devel(libdw)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libssl)
BuildRequires:	devel(libarchive)
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

%package -n udev
Summary:	Device node creation tool
Group:		System

%description -n udev
Device node creation tool

udev creates the device nodes in /dev. Unless you build a different
solution or use a prepopulated static /dev, this is vital for the
OS to work.

%package ukify
Summary:	Tool for working for Unified Kernel Image EFI images
Group:		System/Configuration/Boot and Init

%description ukify
Tool for working for Unified Kernel Image EFI images

%if %{with bootloader}
%package boot
Summary:	EFI boot component for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Requires:	%{name}-ukify = %{EVRD}
Requires:	efi-filesystem
Conflicts:	%{name} < 235-9
Conflicts:	%{name} < 245.20200426-3
Suggests:	%{name}-documentation
Suggests:	%{name}-locale
# (tpg) for logo bootctl/splash-omv.bmp
Suggests:	distro-release-theme
Suggests:	imagemagick
#
Obsoletes:	gummiboot < 46
Provides:	bootloader

%description boot
Systemd boot tools to manage EFI boot.
%endif

%package console
Summary:	Console support for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
# need for /sbin/setfont etc
Requires(meta):	kbd
Conflicts:	%{name} < 235-9
Suggests:	%{name}-documentation
Suggests:	%{name}-locale

%description console
Some systemd units and udev rules are useful only when
you have an actual console, this subpackage contains
these units.

%package networkd
Summary:	Network manager for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
# (tpg) guess what, on some minimal installations systemd-networkd wins over NM
%ifnarch %{armx} %{riscv}
Conflicts:	networkmanager
%endif

%description networkd
A network manager for %{name}.

%{name}-networkd should not be used alongside NetworkManager
(which is the default in OpenMandriva).

Install and use with care.

%package coredump
Summary:	Coredump component for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 235-9
Suggests:	%{name}-documentation
Suggests:	%{name}-locale

%description coredump
Systemd coredump tools to manage coredumps and backtraces.

%package documentation
Summary:	Man pages and documentation for %{name}
Group:		Books/Computer books
Requires:	%{name} >= %{EVRD}
Suggests:	%{name}-locale

%description documentation
Man pages and documentation for %{name}.

%package hwdb
Summary:	hwdb component for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Suggests:	%{name}-polkit
Suggests:	%{name}-documentation
Suggests:	%{name}-locale

%description hwdb
Hardware database management tool for %{name}.

%package locale
Summary:	Translations component for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 235-9

%description locale
Translations for %{name}.

%package polkit
Summary:	PolKit component for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 235-9

%description polkit
PolKit support for %{name}.

%package container
Summary:	Tools for containers and VMs
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Requires:	%{libnss_mymachines} >= %{EVRD}
Conflicts:	%{name} < 235-1
Suggests:	%{name}-polkit
Suggests:	%{name}-bash-completion
Suggests:	%{name}-zsh-completion

%description container
Systemd tools to spawn and manage containers and virtual machines.
This package contains systemd-nspawn, machinectl, systemd-machined,
and systemd-importd.

%package analyze
Summary:	Tools for containers and VMs
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 238-4

%description analyze
Systemd tools to analyze and debug a running system:
systemd-analyze
systemd-cgls
systemd-cgtop
systemd-delta

%package journal-remote
Summary:	Gateway for serving journal events over the network using HTTP
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
%systemd_requires
Obsoletes:	systemd < 206-7
%rename %{name}-journal-gateway

%description journal-remote
Offers journal events over the network using HTTP.

%package cryptsetup
Summary:	Cryptsetup generators for %{name}
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}
Conflicts:	%{name} < 238-4

%description cryptsetup
Systemd generators for cryptsetup (Luks encryption and verity).

%package portable
Summary:	Tools for working with Portable Service Images
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}

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

%package sysext
Summary:	System extension manager
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}

%description sysext
systemd-sysext activates/deactivates system extension images. System extension
images may – dynamically at runtime — extend the /usr/ and /opt/ directory
hierarchies with additional files.

This is particularly useful on immutable system images where a /usr/ and/or
/opt/ hierarchy residing on a read-only file system shall be extended
temporarily at runtime without making any persistent modifications.

%package repart
Summary:	Automatically grow and add partitions
Group:		System/Configuration/Boot and Init
Requires:	%{name} >= %{EVRD}

%description repart
systemd-repart grows and adds partitions to a partition table,
based on the configuration files described in repart.d(5).

%package resolved
Summary:	Daemon for resolving internet host names
Group:		Internet
Requires:	%{name} = %{EVRD}
Recommends:	%{libnss_resolve} = %{EVRD}

%description resolved
Daemon for resolving internet host names

%package homed
Summary:	Home Area/User Account Manager
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{EVRD}
Recommends:	%{name}-polkit >= %{EVRD}

%description homed
systemd-homed is a system service that may be used to create, remove,
change or inspect home areas (directories and network mounts and real
or loopback block devices with a filesystem, optionally encrypted).

%package -n %{libsystemd}
Summary:	Systemd library package
Group:		System/Libraries
%rename		%{oldlibsystemd}

%description -n %{libsystemd}
This package provides the systemd shared library.

%package -n %{libsystemd_devel}
Summary:	Systemd library development files
Group:		Development/C
Requires:	%{name}-rpm-macros = %{EVRD}
Requires:	%{libsystemd} = %{EVRD}

%description -n %{libsystemd_devel}
Development files for the systemd shared library.

%package -n %{libnss_myhostname}
Summary:	Library for local system host name resolution
Group:		System/Libraries
Provides:	libnss_myhostname = %{EVRD}
Provides:	nss_myhostname = %{EVRD}
%rename		%{oldlibnss_myhostname}

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
%rename		%{oldlibnss_mymachines}

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
Provides:	nss_resolve = %{EVRD}
Requires:	%{name} = %{EVRD}
Requires:	%{name}-resolved = %{EVRD}
Conflicts:	%{libnss_myhostname} < 235
%rename		%{oldlibnss_resolve}

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
%rename		%{oldlibnss_systemd}

%description -n %{libnss_systemd}
nss-systemd is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc), providing UNIX user and 
group name resolution for dynamic users and groups allocated through 
the DynamicUser= option in systemd unit files. See systemd.exec(5) 
for details on this option.

%package -n %{libudev}
Summary:	Library for udev
Group:		System/Libraries
%rename		%{oldlibudev}

%description -n %{libudev}
Library for udev.

%package -n %{libudev_devel}
Summary:	Devel library for udev
Group:		Development/C
License:	LGPLv2+
Provides:	udev-devel = %{EVRD}
Requires:	%{libudev} = %{EVRD}
Requires:	%{name}-rpm-macros = %{EVRD}

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
Requires:	bash-completion

%description bash-completion
This package contains bash completion.

%package rpm-macros
Summary:	A RPM macros
Group:		Development/Other
%rename	%{name}-macros

%description rpm-macros
For building RPM packages to utilize standard systemd runtime macros.

%if %{with compat32}
%package -n %{lib32systemd}
Summary:	Systemd library package (32-bit)
Group:		System/Libraries
%rename		%{oldlib32systemd}

%description -n %{lib32systemd}
This package provides the systemd shared library.

%package -n %{lib32systemd_devel}
Summary:	Systemd library development files (32-bit)
Group:		Development/C
Requires:	%{name}-rpm-macros = %{EVRD}
Requires:	%{lib32systemd} = %{EVRD}
Requires:	%{libsystemd_devel} = %{EVRD}

%description -n %{lib32systemd_devel}
Development files for the systemd shared library.

%package -n %{lib32nss_myhostname}
Summary:	Library for local system host name resolution (32-bit)
Group:		System/Libraries
%rename		%{oldlib32nss_myhostname}

%description -n %{lib32nss_myhostname}
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%package -n %{lib32nss_systemd}
Summary:	Provide UNIX user and group name resolution for dynamic users and groups (32-bit)
Group:		System/Libraries
%rename		%{oldlib32nss_systemd}

%description -n %{lib32nss_systemd}
nss-systemd is a plug-in module for the GNU Name Service Switch (NSS) 
functionality of the GNU C Library (glibc), providing UNIX user and 
group name resolution for dynamic users and groups allocated through 
the DynamicUser= option in systemd unit files. See systemd.exec(5) 
[5~for details on this option.

%package -n %{lib32udev}
Summary:	Library for udev (32-bit)
Group:		System/Libraries
%rename		%{oldlib32udev}

%description -n %{lib32udev}
Library for udev.

%package -n %{lib32udev_devel}
Summary:	Devel library for udev (32-bit)
Group:		Development/C
License:	LGPLv2+
Requires:	%{libudev_devel} = %{EVRD}
Requires:	%{lib32udev} = %{EVRD}
Requires:	%{name}-rpm-macros = %{EVRD}

%description -n %{lib32udev_devel}
Devel library for udev.
%endif

%package oom
Summary:	Out of Memory handler
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{EVRD}

%description oom
Out of Memory handler.

%package integritysetup
Summary:	System integrity checker
Group:		System/Configuration/Boot and Init
Requires:	%{name} = %{EVRD}

%description integritysetup
System integrity checker.

%prep
%autosetup -p1 -n systemd-%{version}

%build
%ifarch %{ix86}
mkdir -p bin
ln -sf %{_bindir}/ld.bfd bin/ld
PATH=$PWD/bin:$PATH
%endif

# In order to switch to cgroup1 it is enough to pass systemd.unified_cgroup_hierarchy=0 via kernel command line.

%if %{with compat32}
%meson32 \
	-Dmode=release \
	-Dacl=disabled \
	-Danalyze=false \
	-Dapparmor=disabled \
	-Daudit=disabled \
	-Dbacklight=false \
	-Dbinfmt=false \
	-Dblkid=disabled \
	-Dbzip2=disabled \
	-Dcoredump=false \
	-Dcreate-log-dirs=false \
	-Defi=false \
	-Denvironment-d=false \
	-Dfdisk=disabled \
	-Dfirstboot=false \
	-Dgnutls=disabled \
	-Dgcrypt=disabled \
	-Dhibernate=false \
	-Dlibfido2=disabled \
	-Dhomed=disabled \
	-Dhostnamed=false \
	-Dhtml=disabled \
	-Dhwdb=false \
	-Dima=false \
	-Dimportd=disabled \
	-Dinitrd=false \
	-Dkernel-install=false \
	-Dkmod=disabled \
	-Dldconfig=false \
	-Dlibcryptsetup=disabled \
	-Dlibcryptsetup-plugins=disabled \
	-Dlocaled=false \
	-Dlogind=false \
	-Dmachined=false \
	-Dman=disabled \
	-Dmicrohttpd=disabled \
	-Dnetworkd=false \
	-Doomd=false \
	-Dp11kit=disabled \
	-Dpamconfdir="%{_sysconfdir}/pam.d" \
	-Dpam=disabled \
	-Dpasswdqc=disabled \
	-Dpolkit=disabled \
	-Dportabled=false \
	-Dpstore=false \
	-Dpwquality=false \
	-Dqrencode=disabled \
	-Dquotacheck=false \
	-Drandomseed=false \
	-Dremote=disabled \
	-Drepart=disabled \
	-Dresolve=false \
	-Drfkill=false \
	-Dseccomp=disabled \
	-Dselinux=disabled \
	-Dsplit-bin=false \
	-Dsupport-url="%{disturl}" \
	-Dsysext=false \
	-Dsysusers=false \
	-Dtests=false \
	-Dtimedated=false \
	-Dtimesyncd=false \
	-Dtmpfiles=false \
	-Dtpm=false \
	-Dtranslations=false \
	-Duserdb=false \
	-Dutmp=false \
	-Dvconsole=false \
	-Dxdg-autostart=false \
	-Dfirst-boot-full-preset=false \
	-Dcryptolib=openssl \
	-Dlibiptc=disabled \
	-Dlibcurl=false \
	-Dbpf-framework=false \
	-Dlz4=false \
	-Dxenctrl=disabled \
	-Dtpm2=disabled \
	-Dxkbcommon=disabled \
	-Dsysupdate=disabled \
	-Dnss-mymachines=disabled \
	-Dnss-resolve=disabled \
	-Dbootloader=disabled \
	-Ddefault-compression=zstd

%ninja_build -C build32
%endif

# FIXME b_lto is disabled on RISC-V because of a "invalid build ID" error at
# compile time (at least crosscompiling from x86_64 to risc-v with clang).
# Last verified: clang 16.0.4, systemd 253.5
%meson \
	-Dmode=release \
	-Dsysvinit-path=%{_initrddir} \
	-Dsysvrcnd-path=%{_sysconfdir}/rc.d \
	-Drc-local=%{_sysconfdir}/rc.d/rc.local \
%if %{with bootloader}
	-Dbootloader=true \
	-Defi=true \
	-Dsbat-distro="%{efi_vendor}" \
	-Dsbat-distro-summary="%{distribution}" \
	-Dsbat-distro-pkgname="%{name}" \
	-Dsbat-distro-version="%{version}-%{release}" \
	-Dsbat-distro-url="%{disturl}" \
%else
	-Dbootloader=false \
	-Defi=false \
%endif
%if %{with bootstrap}
	-Dlibcryptsetup=false \
	-Dlibcryptsetup-plugins=false \
%else
	-Dlibcryptsetup=true \
	-Dlibcryptsetup-plugins-dir="%{_libdir}/cryptsetup" \
%endif
%if %{cross_compiling}
	-Ddbussystemservicedir="%{_datadir}/dbus-1/system-services" \
	-Ddbussessionservicedir="%{_datadir}/dbus-1/services" \
	-Ddbuspolicydir="%{_datadir}/dbus-1/system.d" \
%endif
	-Dsplit-bin=false \
	-Dxkbcommon=true \
	-Dtpm=true \
	-Ddev-kvm-mode=0666 \
	-Dkmod=true \
	-Dxkbcommon=true \
	-Dblkid=true \
	-Dfdisk=true \
	-Dpwquality=true \
	-Drepart=true \
%if %{with bootstrap}
	-Dhomed=false \
%else
	-Dhomed=true \
%endif
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
	-Dbzip2=disabled \
	-Dlz4=false \
	-Ddefault-compression=zstd \
	-Dpam=true \
	-Dpamconfdir="%{_sysconfdir}/pam.d" \
	-Dpamlibdir="%{_libdir}/security" \
	-Dacl=true \
	-Dsmack=true \
	-Dgcrypt=false \
	-Daudit=false \
	-Delfutils=true \
	-Dqrencode=true \
	-Dgnutls=true \
	-Dmicrohttpd=true \
	-Dlibidn2=true \
	-Dlibiptc=disabled \
	-Dlibcurl=true \
	-Dtpm=true \
	-Dhwdb=true \
	-Dsysusers=true \
	-Dsysupdate=false \
	-Dman=true \
	-Dhtml=true \
	-Dtests=unsafe \
	-Dinstall-tests=false \
%ifnarch %{riscv}
	-Db_lto=true \
%else
	-Db_lto=false \
%endif
	-Dloadkeys-path=%{_bindir}/loadkeys \
	-Dsetfont-path=%{_bindir}/setfont \
	-Dcertificate-root="%{_sysconfdir}/pki" \
	-Dfallback-hostname="localhost" \
	-Dsupport-url="%{disturl}" \
	-Dtty-gid=5 \
	-Dusers-gid=100 \
	-Dnobody-user=nobody \
	-Dnobody-group=nogroup \
	-Dsystem-uid-max='999' \
	-Dsystem-gid-max='999' \
	-Ddefault-dnssec=no \
	-Dntp-servers='_gateway gateway 0.openmandriva.pool.ntp.org 1.openmandriva.pool.ntp.org 2.openmandriva.pool.ntp.org 3.openmandriva.pool.ntp.org' \
	-Ddns-servers='208.67.222.222 208.67.220.220' \
	-Dadm-gid=4 \
	-Daudio-gid=81 \
	-Dcdrom-gid=22 \
	-Ddialout-gid=83 \
	-Ddisk-gid=6 \
	-Dinput-gid=101 \
	-Dkmem-gid=9 \
	-Dkvm-gid=36 \
	-Dlp-gid=7 \
	-Drender-gid=105 \
	-Dsgx-gid=106 \
	-Dtape-gid=21 \
	-Dtty-gid=5 \
	-Dusers-gid=100 \
	-Dutmp-gid=24 \
	-Dvideo-gid=82 \
	-Dwheel-gid=10 \
	-Dsystemd-journal-gid=190 \
	-Dsystemd-network-uid=194 \
	-Dsystemd-resolve-uid=191 \
	-Dfirst-boot-full-preset=true \
	-Dstatus-unit-format-default=combined \
	-Dcompat-mutable-uid-boundaries=true \
	-Dcryptolib=openssl \
	-Dxenctrl=disabled \
	-Dlibfido2=disabled \
	-Dbpf-framework=true
# -Dsystemd-timesync-uid=, not set yet

%meson_build

%if %{cross_compiling}
# We need a host systemd-hwdb and journalctl to initialize
# hwdb and journal files in %%install
unset CC
unset CXX
unset LD
unset CFLAGS
unset CXXFLAGS
unset LDFLAGS
meson setup \
	-Dmode=release \
	-Defi=false \
	-Dhwdb=true \
	build-native
%ninja_build -C build-native
%endif

%install
%if %{with compat32}
%ninja_install -C build32
rm -rf %{buildroot}%{_sysconfdir} %{buildroot}/lib/{systemd,modprobe.d,udev} %{buildroot}%{_datadir}/{dbus-1,factory,polkit-1}
# (tpg) remove as PAM is not enabled with 32 bit build
rm -rf %{buildroot}%{_sysconfdir}/pam.d
rm -rf %{buildroot}%{_prefix}/lib/{sysusers.d,tmpfile.d,sysctl.d,kernel,systemd/catalog}
%endif
%meson_install

# (bor) create late shutdown and sleep directory
mkdir -p %{buildroot}%{systemd_libdir}/system-shutdown
mkdir -p %{buildroot}%{systemd_libdir}/system-sleep

ln -s loginctl %{buildroot}%{_bindir}/%{name}-loginctl

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the user deleted
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
mkdir -p %{buildroot}/%{systemd_libdir}/system/sound.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/system-update.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/user/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/user/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/user/sockets.target.wants

# And the default symlink we generate automatically based on inittab
rm -f %{buildroot}%{_sysconfdir}/%{name}/system/default.target

# (bor) make sure we own directory for bluez to install service
mkdir -p %{buildroot}/%{systemd_libdir}/system/bluetooth.target.wants

# (tpg) use systemd's own mounting capability
sed -i -e 's/^#MountAuto=yes$/MountAuto=yes/' %{buildroot}/etc/%{name}/system.conf
sed -i -e 's/^#SwapAuto=yes$/SwapAuto=yes/' %{buildroot}/etc/%{name}/system.conf

# (eugeni) install /run
mkdir %{buildroot}/run

# (tpg) create missing dir
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
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/catalog
touch %{buildroot}%{_localstatedir}/lib/systemd/catalog/database
touch %{buildroot}%{_localstatedir}/lib/systemd/random-seed
mkdir -p %{buildroot}%{_localstatedir}/lib/systemd/timesync
touch %{buildroot}%{_localstatedir}/lib/systemd/timesync/clock

# (tpg) needed for containers
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/nspawn

# (cg) Set up the pager to make it generally more useful
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh << EOF
export SYSTEMD_PAGER="%{_bindir}/less -FR"
EOF
chmod 644 %{buildroot}%{_sysconfdir}/profile.d/40systemd.sh

# Install logdir for journald
install -m 0755 -d %{buildroot}%{_logdir}/journal

#
install -m 0755 -d %{buildroot}%{_sysconfdir}/%{name}/network
install -m644 -D %{SOURCE20} %{buildroot}%{_sysconfdir}/%{name}/network/20-wired.network

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
install -m 0644 %{SOURCE18} %{buildroot}%{systemd_libdir}/user-preset/

# (tpg) remove 90-systemd-preset as it is included in ours 90-default.preset
rm -rf %{buildroot}%{systemd_libdir}/system-preset/90-systemd.preset

# Install rsyslog fragment
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/rsyslog.d/

# (tpg) silent kernel messages
# print only KERN_ERR and more serious alerts
echo "kernel.printk = 2 2 2 2" >> %{buildroot}%{_prefix}/lib/sysctl.d/50-default.conf

# (tpg) by default enable SysRq
sed -i -e 's/^#kernel.sysrq = 0/kernel.sysrq = 1/' %{buildroot}%{_prefix}/lib/sysctl.d/50-default.conf

# (tpg) use 100M as a default maximum value for journal logs
sed -i -e 's/^#SystemMaxUse=.*/SystemMaxUse=100M/' %{buildroot}%{_sysconfdir}/%{name}/journald.conf

# systemd-oomd default configuration
install -Dm0644 -t %{buildroot}%{systemd_libdir}/oomd.conf.d/ %{SOURCE26}
install -Dm0644 -t %{buildroot}%{systemd_libdir}/system/system.slice.d/ %{SOURCE27}
install -Dm0644 -t %{buildroot}%{_prefix}/lib/%{name}/user/slice.d/ %{SOURCE27}
install -Dm0644 -t %{buildroot}%{systemd_libdir}/system/service.d/ %{SOURCE28}
sed -r 's|/system/|/user/|g' %{SOURCE28} > 10-timeout-abort.conf.user
install -Dm0644 10-timeout-abort.conf.user %{buildroot}%{_prefix}/lib/%{name}/user/service.d/10-timeout-abort.conf

# rpm doesn't seem to like comments in sysuser files
sed -i -e '/^#/d' %{buildroot}%{_sysusersdir}/*.conf

# systemd-creds
mkdir -p %{buildroot}%{_sysconfdir}/credstore
mkdir -p %{buildroot}%{_sysconfdir}/credstore.encrypted
mkdir -p %{buildroot}%{_prefix}/lib/credstore
mkdir -p %{buildroot}%{_prefix}/lib/credstore.encrypted

%ifarch %{efi}
install -m644 -D %{SOURCE21} %{buildroot}%{_datadir}/%{name}/bootctl/loader.conf
install -m644 -D %{SOURCE22} %{buildroot}%{_datadir}/%{name}/bootctl/omv.conf
# this is ghost file, as we will generate it on systemd-boot install/update
touch %{buildroot}%{_datadir}/%{name}/bootctl/splash-omv.bmp
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

mkdir -p %{buildroot}%{_prefix}/lib/firmware/updates
mkdir -p %{buildroot}%{_sysconfdir}/udev/agents.d/usb
touch %{buildroot}%{_sysconfdir}/scsi_id.config

ln -s udevadm %{buildroot}%{_bindir}/udevd
ln -s %{_bindir}/udevadm %{buildroot}%{udev_libdir}/udevd

mkdir -p %{buildroot}%{_prefix}/lib/firmware/updates
# default /dev content, from Fedora RPM
mkdir -p %{buildroot}%{udev_libdir}/devices/{net,hugepages,pts,shm}
# From previous Mandriva /etc/udev/devices.d
mkdir -p %{buildroot}%{udev_libdir}/devices/cpu/0

# Steam links to "libudev.so.0"...
ln -s libudev.so.%{udev_major} %{buildroot}%{_libdir}/libudev.so.0

#################
#	UDEV	#
#	END	#
#################

# https://bugzilla.redhat.com/show_bug.cgi?id=1378974
install -Dm0644 -t %{buildroot}%{systemd_libdir}/system/systemd-udev-trigger.service.d/ %{SOURCE23}

%if %{cross_compiling}
b=./build-native/
%else
b=./build/
%endif

# Pre-generate and pre-ship hwdb, to speed up first boot
$b/systemd-hwdb --root %{buildroot} --usr update || $b/udevadm hwdb --root %{buildroot} --update --usr

# Compute catalog
$b/journalctl --root %{buildroot} --update-catalog

%if ! %{with bootloader}
# bootctl gets built, but isn't useful, without systemd-boot
rm %{buildroot}%{_bindir}/bootctl
%endif

%if %{cross_compiling}
# For some reason, bash-completion paths are sometimes detected
# incorrectly when cross-compiling even though the pkgconfig
# file looks ok
if [ -d %{buildroot}%{_prefix}%{_target_platform} ]; then
	mv %{buildroot}%{_prefix}/%{_target_platform}%{_datadir}/bash-completion %{buildroot}%{_datadir}
	rm -rf %{buildroot}%{_prefix}/%{_target_platform}
fi
%endif

%find_lang %{name}

# These used to be created because the utmp runlevel logging service
# was there -- that doesn't exist anymore, but this package is probably
# still the most reasonable place to own these directories
mkdir -p %{buildroot}%{_unitdir}/graphical.target.wants
mkdir -p %{buildroot}%{_unitdir}/rescue.target.wants

%include %{SOURCE1}

%triggerin -- glibc
# reexec daemon on self or glibc update to avoid busy / on shutdown
# trigger is executed on both self and target install so no need to have
# extra own post
if [ $1 -ge 2 ] || [ $2 -ge 2 ]; then
    %{_bindir}/systemctl daemon-reexec 2>&1 || :
fi

%post
%{_bindir}/systemd-firstboot --setup-machine-id &>/dev/null ||:
%{_bindir}/systemd-machine-id-setup &>/dev/null ||:
%{_bindir}/systemctl daemon-reexec &>/dev/null ||:

if [ $1 -eq 1 ]; then
    [ -w %{_localstatedir} ] && mkdir -p %{_localstatedir}/log/journal
    %{_bindir}/systemd-sysusers &>/dev/null ||:
    %{systemd_libdir}/systemd-random-seed save &>/dev/null ||:
    %{_bindir}/journalctl --update-catalog &>/dev/null ||:
    %{_bindir}/systemd-tmpfiles --create &>/dev/null ||:

# Init 90-default.preset only on first install
    %{_bindir}/systemctl preset-all &>/dev/null ||:
    %{_bindir}/systemctl --global preset-all &>/dev/null ||:
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

%post resolved
if [ $1 -eq 1 ]; then
# (tpg) link to resolv.conf from systemd
    if [ ! -e /etc/resolv.conf ] && [ ! -L /etc/resolv.conf ]; then
	ln -sf ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf ||:
    elif [ -d /run/systemd/system ] && ! mountpoint /etc/resolv.conf &>/dev/null; then
	ln -fsv ../run/systemd/resolve/stub-resolv.conf /etc/resolv.conf ||:
    fi

    if [ ! -e /run/systemd/resolve/resolv.conf ] || [ ! -e /run/systemd/resolve/stub-resolv.conf ]; then
	[ ! -d /run/systemd/resolve ] && mkdir -p /run/systemd/resolve
	printf '%s\n' "nameserver 208.67.222.222" "nameserver 208.67.220.220" > /run/systemd/resolve/resolv.conf
	printf '%s\n' "nameserver 208.67.222.222" "nameserver 208.67.220.220" > /run/systemd/resolve/stub-resolv.conf
    fi
    %systemd_post systemd-resolved.service
fi

%preun
%systemd_preun systemd-udev{d,-settle,-trigger}.service systemd-udevd-{control,kernel}.socket systemd-timesyncd.service

%postun
if [ $1 -eq 1 ]; then
    [ -w %{_localstatedir} ] && journalctl --update-catalog || :
    systemd-tmpfiles --create &>/dev/null || :
fi

%systemd_postun_with_restart systemd-timedated.service systemd-portabled.service systemd-homed.service systemd-hostnamed.service systemd-journald.service systemd-localed.service systemd-userdbd.service systemd-oomd.service systemd-udevd.service systemd-timesyncd.service

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

%triggerin -- %{libnss_myhostname} < 237
if [ -f /etc/nsswitch.conf ]; then
# sed-fu to add myhostname to hosts line
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
fi

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

%files
%dir %{_prefix}/lib/firmware
%dir %{_prefix}/lib/firmware/updates
%dir %{_prefix}/lib/modprobe.d
%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%dir %{_datadir}/%{name}
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/environment.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.d
%dir %{_prefix}/lib/%{name}/catalog
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
%dir %{_sysconfdir}/credstore
%dir %{_sysconfdir}/credstore.encrypted
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/system
%dir %{_sysconfdir}/%{name}/system/getty.target.wants
%dir %{_sysconfdir}/%{name}/user
%dir %{_sysconfdir}/%{name}/user-preset
%dir %{_sysconfdir}/%{name}/user/default.target.wants
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_libdir}/systemd
%dir %{systemd_libdir}
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
%dir %{systemd_libdir}/system/sockets.target.wants
%dir %{systemd_libdir}/system/sysinit.target.wants
%dir %{systemd_libdir}/system/syslog.target.wants
%dir %{systemd_libdir}/system/halt.target.wants
%dir %{systemd_libdir}/system/initrd-switch-root.target.wants
%dir %{systemd_libdir}/system/initrd.target.wants
%dir %{systemd_libdir}/system/kexec.target.wants
%dir %{systemd_libdir}/system/poweroff.target.wants
%dir %{systemd_libdir}/system/reboot.target.wants
%dir %{systemd_libdir}/system/sound.target.wants
%dir %{systemd_libdir}/system/system-update.target.wants
%dir %{systemd_libdir}/system/timers.target.wants
%dir %{systemd_libdir}/system/machines.target.wants
%dir %{systemd_libdir}/system/remote-fs.target.wants
%dir %{systemd_libdir}/system/user-.slice.d
%dir %{_localstatedir}/lib/systemd
%dir %{_localstatedir}/lib/systemd/catalog
%ghost %{_localstatedir}/lib/systemd/catalog/database
%ghost %attr(0600,root,root) %{_localstatedir}/lib/systemd/random-seed
%ghost %dir %{_localstatedir}/lib/systemd/timesync
%ghost %{_localstatedir}/lib/systemd/timesync/clock
%dir %{_prefix}/lib/credstore
%dir %{_prefix}/lib/credstore.encrypted
%ghost %config(noreplace,missingok) %attr(0644,root,root) %{_sysconfdir}/scsi_id.config
%ghost %config(noreplace) %{_sysconfdir}/hostname
%ghost %config(noreplace) %{_sysconfdir}/locale.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%ghost %config(noreplace) %{_sysconfdir}/machine-info
%ghost %config(noreplace) %{_sysconfdir}/timezone
%ghost %config(noreplace) %{_sysconfdir}/vconsole.conf
%ghost %config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/00-keyboard.conf
%doc %{_prefix}/lib/modprobe.d/README
%doc %{_prefix}/lib/sysctl.d/README
%doc %{_prefix}/lib/sysusers.d/README
%doc %{_prefix}/lib/tmpfiles.d/README
%{_datadir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timesync1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.timesync1.policy
%{_datadir}/polkit-1/actions/io.systemd.credentials.policy
%{_prefix}/lib/%{name}/user-generators/systemd-xdg-autostart-generator
%{_libdir}/security/pam_systemd.so
%{_bindir}/halt
%{_bindir}/journalctl
%{_bindir}/loginctl
%{_bindir}/poweroff
%{_bindir}/reboot
%{_bindir}/systemctl
%{_bindir}/varlinkctl
%{_bindir}/%{name}-ask-password
%{_bindir}/%{name}-escape
%{_bindir}/%{name}-firstboot
%{_bindir}/%{name}-inhibit
%{_bindir}/%{name}-machine-id-setup
%{_bindir}/%{name}-notify
%{_bindir}/%{name}-sysusers
%{_bindir}/%{name}-tmpfiles
%{_bindir}/%{name}-tty-ask-password-agent
%{_bindir}/%{name}-creds
%{_bindir}/systemd-vpick
%{systemd_libdir}/system/sockets.target.wants/systemd-creds.socket
%{systemd_libdir}/system/systemd-creds.socket
%{systemd_libdir}/system/systemd-creds@.service
%{_bindir}/userdbctl
%{_bindir}/init
%{_bindir}/shutdown
%{_bindir}/busctl
%{_bindir}/hostnamectl
%{_bindir}/kernel-install
%{_bindir}/localectl
%{_bindir}/mount.ddi
%{_bindir}/systemd-ac-power
%{_bindir}/systemd-cat
%{_bindir}/systemd-confext
%{_bindir}/systemd-detect-virt
%{_bindir}/systemd-dissect
%{_bindir}/systemd-id128
%{_bindir}/systemd-loginctl
%{_bindir}/systemd-mount
%{_bindir}/systemd-path
%{_bindir}/systemd-run
%{_bindir}/run0
%{_sysconfdir}/pam.d/systemd-run0
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
%{_datadir}/factory/etc/locale.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/%{name}/kbd-model-map
%{_datadir}/%{name}/language-fallback-map
%{_initrddir}/README
%{_prefix}/lib/modprobe.d/systemd.conf
%{_prefix}/lib/kernel/install.d/*.install
%{_prefix}/lib/environment.d/99-environment.conf
%dir %{systemd_libdir}/profile.d
%{systemd_libdir}/profile.d/70-systemd-shell-extra.sh
%{_prefix}/lib/%{name}/*/service.d/10-timeout-abort.conf
%{_prefix}/lib/%{name}/system/user*.service.d/10-login-barrier.conf
%{_prefix}/lib/%{name}/user-preset/*.preset
%{_prefix}/lib/%{name}/user/*.service
%{_prefix}/lib/%{name}/user/*.target
%{_prefix}/lib/%{name}/user/*.timer
%{_prefix}/lib/%{name}/user/*.slice
%{systemd_libdir}/user-environment-generators/*
%{_prefix}/lib/tmpfiles.d/*.conf
%{_datadir}/factory/etc/issue
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/profile.d/70-systemd-shell-extra.sh
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/xdg/%{name}
%dir %{systemd_libdir}/ntp-units.d
%{systemd_libdir}/ntp-units.d/80-systemd-timesync.list
%{systemd_libdir}/systemd-battery-check
%{systemd_libdir}/systemd-executor
%{systemd_libdir}/system/systemd-hibernate-resume.service
%ifarch %{efi}
%{systemd_libdir}/system/sysinit.target.wants/systemd-hibernate-clear.service
%{systemd_libdir}/system/systemd-hibernate-clear.service
%endif
%{_sysconfdir}/ssh/sshd_config.d/20-systemd-userdb.conf
%{systemd_libdir}/sshd_config.d/20-systemd-userdb.conf
# Generators
%dir %{systemd_libdir}/system-generators
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
%{systemd_libdir}/system/rc-local.service
%{systemd_libdir}/system/rescue.service
%{systemd_libdir}/system/system-update-cleanup.service
%{systemd_libdir}/system/systemd-ask-password-console.service
%{systemd_libdir}/system/systemd-ask-password-wall.service
%{systemd_libdir}/system/systemd-backlight@.service
%{systemd_libdir}/system/systemd-battery-check.service
%{systemd_libdir}/system/systemd-binfmt.service
%{systemd_libdir}/system/systemd-boot-check-no-failures.service
%{systemd_libdir}/system/systemd-confext.service
%{systemd_libdir}/system/systemd-exit.service
%{systemd_libdir}/system/systemd-firstboot.service
%{systemd_libdir}/system/systemd-fsck-root.service
%{systemd_libdir}/system/systemd-fsck@.service
%{systemd_libdir}/system/systemd-growfs-root.service
%{systemd_libdir}/system/systemd-growfs@.service
%{systemd_libdir}/system/systemd-halt.service
%{systemd_libdir}/system/systemd-hibernate.service
%{systemd_libdir}/system/systemd-hostnamed.service
%{systemd_libdir}/system/sockets.target.wants/systemd-hostnamed.socket
%{systemd_libdir}/system/systemd-hostnamed.socket
%{systemd_libdir}/system/systemd-hybrid-sleep.service
%{systemd_libdir}/system/systemd-journal-catalog-update.service
%{systemd_libdir}/system/systemd-journal-flush.service
%{systemd_libdir}/system/systemd-journald.service
%{systemd_libdir}/system/systemd-journald@.service
%{systemd_libdir}/system/systemd-journald-sync@.service
%{systemd_libdir}/system/systemd-kexec.service
%{systemd_libdir}/system/systemd-localed.service
%{systemd_libdir}/system/systemd-logind.service
%{systemd_libdir}/system/systemd-machine-id-commit.service
%{systemd_libdir}/system/systemd-modules-load.service
%{systemd_libdir}/system/systemd-journald-audit.socket
%{systemd_libdir}/system/systemd-poweroff.service
%{systemd_libdir}/system/systemd-pstore.service
%{systemd_libdir}/system/systemd-random-seed.service
%{systemd_libdir}/system/systemd-reboot.service
%{systemd_libdir}/system/systemd-remount-fs.service
%{systemd_libdir}/system/systemd-rfkill.service
%{systemd_libdir}/system/systemd-soft-reboot.service
%{systemd_libdir}/system/systemd-suspend-then-hibernate.service
%{systemd_libdir}/system/systemd-suspend.service
%{systemd_libdir}/system/systemd-sysctl.service
%{systemd_libdir}/system/systemd-sysusers.service
%{systemd_libdir}/system/systemd-time-wait-sync.service
%{systemd_libdir}/system/systemd-timedated.service
%{systemd_libdir}/system/systemd-timesyncd.service
%{systemd_libdir}/system/systemd-tmpfiles-clean.service
%{systemd_libdir}/system/systemd-tmpfiles-setup-dev.service
%{systemd_libdir}/system/systemd-tmpfiles-setup-dev-early.service
%{systemd_libdir}/system/systemd-tmpfiles-setup.service
%{systemd_libdir}/system/systemd-udev-load-credentials.service
%{systemd_libdir}/system/systemd-udev-settle.service
%{systemd_libdir}/system/systemd-udev-trigger.service
%{systemd_libdir}/system/systemd-udevd.service
%{systemd_libdir}/system/systemd-update-done.service
%{systemd_libdir}/system/systemd-update-utmp.service
%{systemd_libdir}/system/systemd-user-sessions.service
%{systemd_libdir}/system/systemd-userdbd.service
%{systemd_libdir}/system/systemd-vconsole-setup.service
%{systemd_libdir}/system/systemd-volatile-root.service
%{systemd_libdir}/system/user-runtime-dir@.service
%{systemd_libdir}/system/user@.service
%{systemd_libdir}/system/capsule.slice
%{systemd_libdir}/system/capsule@.service
# Sockets
%{systemd_libdir}/system/syslog.socket
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
%{systemd_libdir}/system/initrd-usr-fs.target
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
%{systemd_libdir}/system/shutdown.target
%{systemd_libdir}/system/sigpwr.target
%{systemd_libdir}/system/sleep.target
%{systemd_libdir}/system/slices.target
%{systemd_libdir}/system/smartcard.target
%{systemd_libdir}/system/sockets.target
%{systemd_libdir}/system/soft-reboot.target
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
%{systemd_libdir}/system/local-fs.target.wants/tmp.mount
%{systemd_libdir}/system/multi-user.target.wants/systemd-ask-password-wall.path
%{systemd_libdir}/system/multi-user.target.wants/systemd-logind.service
%{systemd_libdir}/system/multi-user.target.wants/systemd-user-sessions.service
%{systemd_libdir}/system/multi-user.target.wants/getty.target
%{systemd_libdir}/system/sockets.target.wants/systemd-journald-dev-log.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-journald.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-udevd-control.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-udevd-kernel.socket
%{systemd_libdir}/system/initrd.target.wants/systemd-battery-check.service
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
%{systemd_libdir}/system/sysinit.target.wants/systemd-tmpfiles-setup-dev-early.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-tmpfiles-setup.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-udev-trigger.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-udevd.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-update-done.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-update-utmp.service
%{systemd_libdir}/system/user-.slice.d/10-defaults.conf
%{systemd_libdir}/system/usb-gadget.target
%{systemd_libdir}/system/timers.target.wants/systemd-tmpfiles-clean.timer
%{systemd_libdir}/systemd
%{systemd_libdir}/systemd-backlight
%{systemd_libdir}/systemd-binfmt
%{systemd_libdir}/systemd-boot-check-no-failures
%{systemd_libdir}/systemd-export
%{systemd_libdir}/systemd-fsck
%{systemd_libdir}/systemd-growfs
%{systemd_libdir}/systemd-hibernate-resume
%{systemd_libdir}/systemd-hostnamed
%{systemd_libdir}/systemd-import-fs
%{systemd_libdir}/systemd-journald
%{systemd_libdir}/systemd-localed
%{systemd_libdir}/systemd-logind
%{systemd_libdir}/systemd-makefs
%{systemd_libdir}/systemd-measure
%{systemd_libdir}/systemd-modules-load
%{systemd_libdir}/systemd-pstore
%{systemd_libdir}/systemd-random-seed
%{systemd_libdir}/systemd-remount-fs
%{systemd_libdir}/systemd-reply-password
%{systemd_libdir}/systemd-rfkill
%{systemd_libdir}/systemd-shutdown
%{systemd_libdir}/systemd-sleep
%{systemd_libdir}/systemd-socket-proxyd
%{systemd_libdir}/systemd-sulogin-shell
%{systemd_libdir}/systemd-sysctl
%{systemd_libdir}/systemd-sysroot-fstab-check
%{systemd_libdir}/systemd-time-wait-sync
%{systemd_libdir}/systemd-timedated
%{systemd_libdir}/systemd-timesyncd
%{systemd_libdir}/systemd-update-done
%{systemd_libdir}/systemd-update-utmp
%{systemd_libdir}/systemd-user-runtime-dir
%{systemd_libdir}/systemd-user-sessions
%{systemd_libdir}/systemd-userdbd
%{systemd_libdir}/systemd-userwork
%if ! %{with bootstrap}
%{systemd_libdir}/systemd-veritysetup
%endif
%{systemd_libdir}/systemd-volatile-root
%{systemd_libdir}/systemd-xdg-autostart-condition
# (tpg) internal libraries - only systemd uses them
%{_libdir}/systemd/libsystemd-core-%{major}.so
%{_libdir}/systemd/libsystemd-shared-%{major}.so
#
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal
%config(noreplace) %{_prefix}/lib/sysctl.d/50-default.conf
# This file exists only on 64-bit arches
%ifnarch %{ix86} %{arm}
%config(noreplace) %{_prefix}/lib/sysctl.d/50-pid-max.conf
%endif
%config(noreplace) %{_prefix}/lib/sysusers.d/basic.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-remote.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-coredump.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-journal.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-network.conf
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-timesync.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
%config(noreplace) %{_sysconfdir}/rsyslog.d/listen.conf
%config(noreplace) %{_sysconfdir}/%{name}/journald.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf
%config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
%config(noreplace) %{_sysconfdir}/%{name}/logind.conf
%config(noreplace) %{_sysconfdir}/%{name}/pstore.conf
%config(noreplace) %{_sysconfdir}/%{name}/sleep.conf
%config(noreplace) %{_sysconfdir}/%{name}/system.conf
%config(noreplace) %{_sysconfdir}/%{name}/timesyncd.conf
%config(noreplace) %{_sysconfdir}/%{name}/user.conf
%config(noreplace) %{_sysconfdir}/dnf/protected.d/systemd.conf
# This takes care of interface renaming etc. -- it is NOT for networkd
%dir %{systemd_libdir}/network
%{systemd_libdir}/network/99-default.link
# New in -250, need to verify if this needs to go to subpackages
%{systemd_libdir}/systemd-update-helper
%{systemd_libdir}/ukify
%{_prefix}/lib/kernel/install.conf
%{_datadir}/mime/packages/io.systemd.xml
# New in -258, need to verify if this needs to go to subpackages
%{_sysconfdir}/profile.d/80-systemd-osc-context.sh
%{_bindir}/systemd-pty-forward
%{systemd_libdir}/import-pubring.pgp
%{systemd_libdir}/initrd-preset/90-systemd.preset
%{systemd_libdir}/initrd-preset/99-default.preset
%{systemd_libdir}/network/80-namespace-ns-tun.link
%{systemd_libdir}/network/80-namespace-ns-tun.network
%{systemd_libdir}/profile.d/80-systemd-osc-context.sh
%{systemd_libdir}/system/breakpoint-pre-basic.service
%{systemd_libdir}/system/breakpoint-pre-mount.service
%{systemd_libdir}/system/breakpoint-pre-switch-root.service
%{systemd_libdir}/system/breakpoint-pre-udev.service
%{systemd_libdir}/system/imports-pre.target
%{systemd_libdir}/system/imports.target
%{systemd_libdir}/system/initrd.target.wants/systemd-confext-initrd.service
%{systemd_libdir}/system/initrd.target.wants/systemd-sysext-initrd.service
%{systemd_libdir}/system/sockets.target.wants/systemd-ask-password.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-logind-varlink.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-machined.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-udevd-varlink.socket
%{systemd_libdir}/system/sysinit.target.wants/imports.target
%{systemd_libdir}/system/systemd-ask-password.socket
%{systemd_libdir}/system/systemd-ask-password@.service
%{systemd_libdir}/system/systemd-confext-initrd.service
%{systemd_libdir}/system/systemd-logind-varlink.socket
%{systemd_libdir}/system/systemd-loop@.service
%{systemd_libdir}/system/systemd-sysext-initrd.service
%{systemd_libdir}/system/systemd-udevd-varlink.socket
%{systemd_libdir}/system/systemd-userdb-load-credentials.service
%{systemd_libdir}/system/systemd-validatefs@.service
%{systemd_libdir}/systemd-ssh-issue
%{systemd_libdir}/systemd-validatefs
%{systemd_libdir}/user/sockets.target.wants/systemd-ask-password.socket
%{systemd_libdir}/user/systemd-ask-password.socket
%{udev_rules_dir}/60-persistent-hidraw.rules
%{udev_rules_dir}/81-net-bridge.rules
%{udev_rules_dir}/90-image-dissect.rules
%{_datadir}/polkit-1/actions/io.systemd.namespace-resource.policy
%{_datadir}/polkit-1/rules.d/10-systemd-logind-root-ignore-inhibitors.rules.example
# factory-reset stuff (should this be a subpackage?)
%{systemd_libdir}/system-generators/systemd-factory-reset-generator
%{systemd_libdir}/system/factory-reset-now.target
%{systemd_libdir}/system/factory-reset.target.wants/systemd-factory-reset-request.service
%{systemd_libdir}/system/sockets.target.wants/systemd-factory-reset.socket
%{systemd_libdir}/system/systemd-factory-reset-complete.service
%{systemd_libdir}/system/systemd-factory-reset-reboot.service
%{systemd_libdir}/system/systemd-factory-reset-request.service
%{systemd_libdir}/system/systemd-factory-reset.socket
%{systemd_libdir}/system/systemd-factory-reset@.service
%{systemd_libdir}/system/factory-reset.target
%{systemd_libdir}/systemd-factory-reset
# D-Bus interfaces
%if ! %{cross_compiling}
%{_datadir}/dbus-1/interfaces/org.freedesktop.LogControl1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.home1.Home.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.home1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.hostname1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.import1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.import1.Transfer.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.locale1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.login1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.login1.Seat.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.login1.Session.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.login1.User.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.machine1.Image.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.machine1.Machine.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.machine1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.network1.DHCPServer.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.network1.Link.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.network1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.network1.Network.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.oom1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.portable1.Image.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.portable1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Automount.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Job.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Mount.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Path.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Scope.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Service.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Slice.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Socket.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Swap.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Target.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Timer.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Unit.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.timedate1.xml
%endif
# New in -259:
%{_bindir}/systemd-mute-console
%{systemd_libdir}/system/sockets.target.wants/systemd-mute-console.socket
%{systemd_libdir}/system/system-systemd\x2dmute\x2dconsole.slice
%{systemd_libdir}/system/systemd-mute-console.socket
%{systemd_libdir}/system/systemd-mute-console@.service
%{systemd_libdir}/system/systemd-networkd-resolve-hook.socket
%{systemd_libdir}/user/sockets.target.wants/systemd-importd.socket
%{systemd_libdir}/user/sockets.target.wants/systemd-machined.socket
%{systemd_libdir}/user/systemd-importd.socket
%{systemd_libdir}/user/systemd-machined.socket
%{_datadir}/polkit-1/rules.d/empower.rules

# Split into a separate package so it can be used in installations
# and containers that don't use systemd
%files -n udev
%doc %{_prefix}/lib/udev/hwdb.d/README
%doc %{_prefix}/lib/udev/rules.d/README
%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/agents.d
%dir %{_sysconfdir}/udev/agents.d/usb
%dir %{_sysconfdir}/udev/rules.d
%dir %{udev_libdir}
%dir %{udev_libdir}/hwdb.d
%dir %{udev_rules_dir}
%{systemd_libdir}/systemd-udevd
%{udev_rules_dir}/10-imx.rules
%{udev_rules_dir}/50-udev-default.rules
%{udev_rules_dir}/50-udev-mandriva.rules
%{udev_rules_dir}/60-autosuspend.rules
%{udev_rules_dir}/60-block.rules
%{udev_rules_dir}/60-block-scheduler.rules
%{udev_rules_dir}/60-fido-id.rules
%{udev_rules_dir}/60-gpiochip.rules
%{udev_rules_dir}/60-infiniband.rules
%{udev_rules_dir}/60-persistent-storage.rules
%{udev_rules_dir}/60-persistent-storage-mtd.rules
%{udev_rules_dir}/60-sensor.rules
%{udev_rules_dir}/60-serial.rules
%{udev_rules_dir}/64-btrfs.rules
%{udev_rules_dir}/69-printeracl.rules
%{udev_rules_dir}/70-camera.rules
%{udev_rules_dir}/70-power-switch.rules
%{udev_rules_dir}/70-uaccess.rules
%{udev_rules_dir}/71-seat.rules
%{udev_rules_dir}/73-seat-late.rules
%{udev_rules_dir}/75-net-description.rules
%{udev_rules_dir}/80-drivers.rules
%{udev_rules_dir}/80-net-setup-link.rules
%{udev_rules_dir}/81-net-dhcp.rules
%{udev_rules_dir}/82-net-auto-link-local.rules
%{udev_rules_dir}/90-iocost.rules
%{udev_rules_dir}/99-systemd.rules
%{_bindir}/udevd
%{_bindir}/udevadm
%{udev_rules_dir}/60-dmi-id.rules
%{_prefix}/lib/udev/dmi_memory_id
%{_prefix}/lib/udev/rules.d/70-memory.rules
%attr(0755,root,root) %{udev_libdir}/ata_id
%attr(0755,root,root) %{udev_libdir}/fido_id
%attr(0755,root,root) %{udev_libdir}/iocost
%attr(0755,root,root) %{udev_libdir}/scsi_id
%{udev_libdir}/udevd
%config(noreplace) %{_sysconfdir}/sysconfig/udev
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%config(noreplace) %{_sysconfdir}/udev/iocost.conf

%files sysext
%{_bindir}/systemd-sysext
%{systemd_libdir}/system/systemd-sysext.service
%{systemd_libdir}/system/sockets.target.wants/systemd-sysext.socket
%{systemd_libdir}/system/systemd-sysext.socket
%{systemd_libdir}/system/systemd-sysext@.service

%files repart
%{_bindir}/systemd-repart
%{systemd_libdir}/repart
%{systemd_libdir}/system/initrd-root-fs.target.wants/systemd-repart.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-repart.service
%{systemd_libdir}/system/sockets.target.wants/systemd-repart.socket
%{systemd_libdir}/system/systemd-repart.service
%{systemd_libdir}/system/systemd-repart.socket
%{systemd_libdir}/system/systemd-repart@.service

%files resolved
%{_bindir}/resolvconf
%{_bindir}/resolvectl
%if ! %{cross_compiling}
%{_datadir}/dbus-1/interfaces/org.freedesktop.resolve1.DnsDelegate.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.resolve1.DnssdService.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.resolve1.Link.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.resolve1.Manager.xml
%endif
%{systemd_libdir}/resolv.conf
%{systemd_libdir}/systemd-resolved
%{systemd_libdir}/system/systemd-resolved.service
%{systemd_libdir}/system/systemd-resolved-monitor.socket
%{systemd_libdir}/system/systemd-resolved-varlink.socket
%config(noreplace) %{_sysconfdir}/%{name}/resolved.conf
# Clients
%{_bindir}/systemd-resolve
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-resolve.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.resolve1.policy

%if ! %{with bootstrap}
%files homed
%{_bindir}/homectl
%{_bindir}/systemd-home-fallback-shell
%config(noreplace) %{_sysconfdir}/systemd/homed.conf
%{systemd_libdir}/system/systemd-homed-activate.service
%{systemd_libdir}/system/systemd-homed.service
%{systemd_libdir}/system/systemd-homed-firstboot.service
%{systemd_libdir}/systemd-homed
%{systemd_libdir}/systemd-homework
%{_libdir}/security/pam_systemd_home.so
%{_datadir}/dbus-1/system-services/org.freedesktop.home1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.home1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.home1.policy
%endif

%if ! %{with bootstrap}
%files integritysetup
%{systemd_libdir}/system-generators/systemd-integritysetup-generator
%{systemd_libdir}/system/sysinit.target.wants/integritysetup.target
%{systemd_libdir}/systemd-integritysetup
%{systemd_libdir}/system/integritysetup.target
%{systemd_libdir}/system/integritysetup-pre.target
%{systemd_libdir}/system/remote-integritysetup.target
%{systemd_libdir}/system/initrd-root-device.target.wants/remote-integritysetup.target
%endif

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
%{_bindir}/portablectl

%files journal-remote
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
%{_bindir}/importctl
%{_datadir}/dbus-1/services/org.freedesktop.import1.service
%{_datadir}/dbus-1/services/org.freedesktop.machine1.service
%{systemd_libdir}/system/dbus-org.freedesktop.import1.service
%{systemd_libdir}/system/dbus-org.freedesktop.machine1.service
%{systemd_libdir}/system/machine.slice
%{systemd_libdir}/system/machines.target
%{systemd_libdir}/system/machines.target.wants/var-lib-machines.mount
%{systemd_libdir}/system/remote-fs.target.wants/var-lib-machines.mount
%{systemd_libdir}/system/systemd-importd.service
%{systemd_libdir}/system/systemd-machined.socket
%{systemd_libdir}/system/systemd-machined.service
%{systemd_libdir}/system/systemd-nspawn@.service
%{systemd_libdir}/system/systemd-vmspawn@.service
%{systemd_libdir}/system/var-lib-machines.mount
%{systemd_libdir}/systemd-import
%{systemd_libdir}/systemd-importd
%{systemd_libdir}/systemd-machined
%{systemd_libdir}/systemd-pull
%{_sysconfdir}/ssh/ssh_config.d/20-systemd-ssh-proxy.conf
%{systemd_libdir}/ssh_config.d/20-systemd-ssh-proxy.conf
%{systemd_libdir}/system/ssh-access.target
%{systemd_libdir}/system-generators/systemd-ssh-generator
%{systemd_libdir}/systemd-ssh-proxy
%dir %{_sysconfdir}/%{name}/nspawn
%{_bindir}/machinectl
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-vmspawn
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.import1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.import1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy
# New in 256
%{systemd_libdir}/network/80-6rd-tunnel.link
%{systemd_libdir}/network/80-container-host0-tun.network
%{systemd_libdir}/network/80-container-vb.link
%{systemd_libdir}/network/80-container-ve.link
%{systemd_libdir}/network/80-container-vz.link
%{systemd_libdir}/network/80-namespace-ns.link
%{systemd_libdir}/network/80-namespace-ns.network
%{systemd_libdir}/network/80-vm-vt.link
# importd
%{systemd_libdir}/system-generators/systemd-import-generator
%{systemd_libdir}/system/sockets.target.wants/systemd-importd.socket
%{systemd_libdir}/system/systemd-importd.socket

%files -n %{libnss_mymachines}
%{_libdir}/libnss_mymachines.so.%{libnss_major}

%files -n %{libnss_myhostname}
%{_libdir}/libnss_myhostname.so.%{libnss_major}*

%files -n %{libnss_resolve}
%{_libdir}/libnss_resolve.so.%{libnss_major}

%files -n %{libnss_systemd}
%{_libdir}/libnss_systemd.so.%{libnss_major}

%files -n %{libsystemd}
%{_libdir}/libsystemd.so.%{libsystemd_major}*

%files -n %{libsystemd_devel}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/_sd-common.h
%{_includedir}/%{name}/sd-bus-protocol.h
%{_includedir}/%{name}/sd-bus-vtable.h
%{_includedir}/%{name}/sd-bus.h
%{_includedir}/%{name}/sd-device.h
%{_includedir}/%{name}/sd-event.h
%{_includedir}/%{name}/sd-gpt.h
%{_includedir}/%{name}/sd-hwdb.h
%{_includedir}/%{name}/sd-id128.h
%{_includedir}/%{name}/sd-journal.h
%{_includedir}/%{name}/sd-json.h
%{_includedir}/%{name}/sd-login.h
%{_includedir}/%{name}/sd-messages.h
%{_includedir}/%{name}/sd-daemon.h
%{_includedir}/%{name}/sd-path.h
%{_includedir}/%{name}/sd-varlink.h
%{_includedir}/%{name}/sd-varlink-idl.h
%{_libdir}/lib%{name}.so
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/lib%{name}.pc

%files -n %{libudev}
%{_libdir}/libudev.so.0
%{_libdir}/libudev.so.%{udev_major}*

%files -n %{libudev_devel}
%{_libdir}/libudev.so
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/udev.pc
%{_includedir}/libudev.h

%files analyze
%{_bindir}/%{name}-analyze
%{_bindir}/%{name}-cgls
%{_bindir}/%{name}-cgtop
%{_bindir}/%{name}-delta

%files ukify
%{_bindir}/ukify
%{_prefix}/lib/kernel/uki.conf

%if %{with bootloader}
%files boot
%{_bindir}/bootctl
%dir %{_prefix}/lib/%{name}/boot
%dir %{_prefix}/lib/%{name}/boot/efi
%dir %{_datadir}/%{name}/bootctl
%{_prefix}/lib/%{name}/boot/efi/*.efi
%{_prefix}/lib/%{name}/boot/efi/*.stub
%{_datadir}/%{name}/bootctl/*.conf
%ghost %{_datadir}/%{name}/bootctl/splash-omv.bmp
# New in 256
%{systemd_libdir}/system/sockets.target.wants/systemd-bootctl.socket
%{systemd_libdir}/system/systemd-bootctl.socket
%{systemd_libdir}/system/systemd-bootctl@.service
# Only built if ENABLE_BOOTLOADER is set, so those *probably* belong here
# File a bug report if they don't.
%{systemd_libdir}/system/factory-reset.target.wants/systemd-pcrphase-factory-reset.service
%{systemd_libdir}/system/systemd-pcrphase-factory-reset.service
%{systemd_libdir}/system/systemd-pcrphase-initrd.service
%{systemd_libdir}/system/systemd-pcrphase-sysinit.service
%{systemd_libdir}/system/systemd-pcrphase.service
%{systemd_libdir}/system/systemd-pcrextend.socket
%{systemd_libdir}/system/systemd-pcrextend@.service
%{systemd_libdir}/system/systemd-tpm2-clear.service
%{systemd_libdir}/system/systemd-tpm2-setup-early.service
%{systemd_libdir}/system/systemd-tpm2-setup.service
%{systemd_libdir}/system/systemd-pcrlock-make-policy.service
%{systemd_libdir}/system/systemd-pcrlock-secureboot-authority.service
%{systemd_libdir}/system/systemd-pcrlock-secureboot-policy.service
%{systemd_libdir}/system/systemd-boot-random-seed.service
%{systemd_libdir}/system/systemd-pcrfs-root.service
%{systemd_libdir}/system/systemd-pcrfs@.service
%{systemd_libdir}/system/systemd-pcrmachine.service
%{systemd_libdir}/system/systemd-boot-update.service
%{systemd_libdir}/system/systemd-bless-boot.service
%{systemd_libdir}/system-generators/systemd-bless-boot-generator
%{systemd_libdir}/system/initrd.target.wants/systemd-pcrphase-initrd.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-boot-random-seed.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-pcrmachine.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-pcrphase-sysinit.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-pcrphase.service
%{systemd_libdir}/systemd-bless-boot
%{systemd_libdir}/system/storage-target-mode.target.wants/systemd-pcrphase-storage-target-mode.service
%{systemd_libdir}/system/systemd-boot-clear-sysfail.service
%{systemd_libdir}/system/systemd-pcrphase-storage-target-mode.service
%{systemd_libdir}/systemd-tpm2-clear
%{systemd_libdir}/systemd-tpm2-setup
%{systemd_libdir}/system/sysinit.target.wants/systemd-tpm2-setup-early.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-tpm2-setup.service
%{systemd_libdir}/system/systemd-pcrlock-file-system.service
%{systemd_libdir}/system/systemd-pcrlock-firmware-code.service
%{systemd_libdir}/system/systemd-pcrlock-firmware-config.service
%{systemd_libdir}/system/systemd-pcrlock-machine-id.service
%{systemd_libdir}/systemd-pcrextend
%{systemd_libdir}/system/sockets.target.wants/systemd-pcrextend.socket
%{systemd_libdir}/system/sockets.target.wants/systemd-pcrlock.socket
%{systemd_libdir}/system/systemd-pcrlock.socket
%{systemd_libdir}/system/systemd-pcrlock@.service
%{_prefix}/lib/nvpcr/cryptsetup.nvpcr
%{_prefix}/lib/nvpcr/hardware.nvpcr
%{systemd_libdir}/system/sysinit.target.wants/systemd-pcrnvdone.service
%{systemd_libdir}/system/sysinit.target.wants/systemd-pcrproduct.service
%{systemd_libdir}/system/systemd-pcrnvdone.service
%{systemd_libdir}/system/systemd-pcrproduct.service
%{systemd_libdir}/system-generators/systemd-tpm2-generator

%post boot
if [ ! -e %{_datadir}/%{name}/bootctl/splash-omv.bmp ] && [ -e %{_datadir}/pixmaps/system-logo-white.png ] && [ -x %{_bindir}/convert ]; then
    convert %{_datadir}/pixmaps/system-logo-white.png -type truecolor %{_datadir}/%{name}/bootctl/splash-omv.bmp
fi

%preun boot
%systemd_preun systemd-boot-update.service}

%postun boot
%systemd_postun_with_restart systemd-boot-update.service
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
%{_datadir}/factory/etc/vconsole.conf

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
%ghost %attr(0444,root,root) %{_sysconfdir}/udev/hwdb.bin
%{systemd_libdir}/system/sysinit.target.wants/systemd-hwdb-update.service
%{systemd_libdir}/system/systemd-hwdb-update.service
%{_bindir}/systemd-hwdb
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

%post hwdb
udevadm hwdb --update &>/dev/null

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
%{_sysconfdir}/%{name}/network/20-wired.network
%{systemd_libdir}/system/systemd-network-generator.service
%{systemd_libdir}/system/systemd-networkd-wait-online.service
%{systemd_libdir}/system/systemd-networkd.service
%{systemd_libdir}/system/systemd-networkd.socket
%{systemd_libdir}/system/systemd-networkd-varlink.socket
%{systemd_libdir}/systemd-network-generator
%{systemd_libdir}/systemd-networkd
%{systemd_libdir}/systemd-networkd-wait-online
%{_datadir}/dbus-1/system.d/org.freedesktop.network1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%optional %{_datadir}/dbus-1/interfaces/org.freedesktop.network1.DHCPv4Client.xml
%optional %{_datadir}/dbus-1/interfaces/org.freedesktop.network1.DHCPv6Client.xml
%{_bindir}/networkctl
%{systemd_libdir}/network/80-container-host0.network
%{systemd_libdir}/network/80-container-vb.network
%{systemd_libdir}/network/80-container-ve.network
%{systemd_libdir}/network/80-container-vz.network
%{systemd_libdir}/network/80-vm-vt.network
%{systemd_libdir}/network/80-wifi-adhoc.network
%{systemd_libdir}/network/80-wifi-ap.network.example
%{systemd_libdir}/network/80-wifi-station.network.example
%{systemd_libdir}/network/80-6rd-tunnel.network
%{systemd_libdir}/network/80-auto-link-local.network.example
%{systemd_libdir}/network/89-ethernet.network.example
%{systemd_libdir}/system/systemd-networkd-wait-online@.service
%{systemd_libdir}/system/systemd-networkd-persistent-storage.service
%{_datadir}/polkit-1/actions/org.freedesktop.network1.policy
%{_datadir}/polkit-1/rules.d/systemd-networkd.rules

%post networkd
%systemd_post systemd-networkd.service systemd-networkd-wait-online.service

%preun networkd
if [ $1 -eq 0 ] ; then
    %{_bindir}/systemctl --quiet disable systemd-networkd.service 2>&1 || :
else
    %systemd_preun systemd-networkd.service systemd-networkd-wait-online.service
fi

%files cryptsetup
%{systemd_libdir}/systemd-keyutil
%{systemd_libdir}/systemd-sbsign
%if !%{with bootstrap}
%{systemd_libdir}/systemd-cryptsetup
%{systemd_libdir}/system-generators/systemd-cryptsetup-generator
%{systemd_libdir}/system-generators/systemd-veritysetup-generator
%{systemd_libdir}/system/sysinit.target.wants/cryptsetup.target
%{systemd_libdir}/system/system-systemd\x2dcryptsetup.slice
%{systemd_libdir}/system/remote-cryptsetup.target
%{systemd_libdir}/system/cryptsetup-pre.target
%{systemd_libdir}/system/cryptsetup.target
%{systemd_libdir}/system/initrd-root-device.target.wants/remote-cryptsetup.target
%{systemd_libdir}/system/initrd-root-device.target.wants/remote-veritysetup.target
%{systemd_libdir}/system/remote-veritysetup.target
%{systemd_libdir}/system/sysinit.target.wants/veritysetup.target
%{systemd_libdir}/system/veritysetup-pre.target
%{systemd_libdir}/system/veritysetup.target
%{systemd_libdir}/system/system-systemd\x2dveritysetup.slice
%{_bindir}/systemd-cryptenroll
%{_bindir}/systemd-cryptsetup
%{_libdir}/cryptsetup/libcryptsetup-token-systemd-pkcs11.so
%{_libdir}/cryptsetup/libcryptsetup-token-systemd-tpm2.so
%endif
%{_libdir}/security/pam_systemd_loadkey.so

%files zsh-completion
%{_datadir}/zsh/site-functions/*

%files bash-completion
%optional %dir %{_datadir}/bash-completion
%optional %dir %{_datadir}/bash-completion/completions
%optional %{_datadir}/bash-completion/completions/*

%files rpm-macros
%{_rpmmacrodir}/macros.systemd

%files oom
%{_bindir}/oomctl
%{_sysconfdir}/systemd/oomd.conf
%dir %{systemd_libdir}/oomd.conf.d
%{systemd_libdir}/oomd.conf.d/10-oomd-defaults.conf
%{systemd_libdir}/system/system.slice.d/10-oomd-per-slice-defaults.conf
%{_prefix}/lib/%{name}/user/slice.d/10-oomd-per-slice-defaults.conf
%{systemd_libdir}/system/systemd-oomd.socket
%{systemd_libdir}/system/systemd-oomd.service
%{systemd_libdir}/systemd-oomd
%config(noreplace) %{_prefix}/lib/sysusers.d/systemd-oom.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.oom1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.oom1.conf

%if %{with compat32}
%files -n %{lib32nss_myhostname}
%{_prefix}/lib/libnss_myhostname.so.*

%files -n %{lib32nss_systemd}
%{_prefix}/lib/libnss_systemd.so.*

%files -n %{lib32systemd}
%{_prefix}/lib/libsystemd.so.*
%{systemd_libdir}/libsystemd-core-%{major}.so
%{systemd_libdir}/libsystemd-shared-%{major}.so

%files -n %{lib32udev}
%{_prefix}/lib/libudev.so.*

%files -n %{lib32systemd_devel}
%{_prefix}/lib/libsystemd.so
%{_prefix}/lib/pkgconfig/libsystemd.pc

%files -n %{lib32udev_devel}
%{_prefix}/lib/libudev.so
%{_prefix}/lib/pkgconfig/libudev.pc
%endif

%package bsod
Summary: Systemd BSOD tool for displaying information about crashes

%description bsod
Systemd BSOD tool for displaying information about crashes

%files bsod
%{systemd_libdir}/systemd-bsod
%{systemd_libdir}/system/systemd-bsod.service
%{systemd_libdir}/system/initrd.target.wants/systemd-bsod.service

%package storage
Summary: Systemd storage mode exporting all storage devices as NVMe-TCP

%description storage
Systemd storage mode exporting all storage devices as NVMe-TCP

%files storage
%{systemd_libdir}/system/storage-target-mode.target
%{systemd_libdir}/system/systemd-storagetm.service
%{systemd_libdir}/systemd-storagetm

%package pcrlock
Summary: PCR measurement predicition files for systemd

%description pcrlock
PCR measurement predicition files for systemd

%files pcrlock
%{systemd_libdir}/systemd-pcrlock
%{systemd_libdir}/system/tpm2.target
%{_prefix}/lib/pcrlock.d

%package mountfsd
Summary: Tool for dissecting raw disk images and returning mountable file descriptors
Provides: varlink(io.systemd.MountFileSystem)

%description mountfsd
Tool for dissecting raw disk images and returning mountable file descriptors

%files mountfsd
%{systemd_libdir}/system/systemd-mountfsd.service
%{systemd_libdir}/system/systemd-mountfsd.socket
%{systemd_libdir}/systemd-mountfsd
%{systemd_libdir}/systemd-mountwork
%{_datadir}/polkit-1/actions/io.systemd.mount-file-system.policy

%package nsresourced
Summary: User Namespace Resource Delegation Service
Provides: varlink(io.systemd.NamespaceResource)

%description nsresourced
User Namespace Resource Delegation Service

%files nsresourced
%{systemd_libdir}/system/systemd-nsresourced.service
%{systemd_libdir}/system/systemd-nsresourced.socket
%{systemd_libdir}/systemd-nsresourced
%{systemd_libdir}/systemd-nsresourcework

%package quota
Summary: Filesystem quota support for systemd

%description quota
Filesystem quota support for systemd

%files quota
%{systemd_libdir}/systemd-quotacheck
%{systemd_libdir}/system/systemd-quotacheck-root.service
%{systemd_libdir}/system/systemd-quotacheck@.service
%{systemd_libdir}/system/quotaon-root.service
%{systemd_libdir}/system/quotaon@.service
