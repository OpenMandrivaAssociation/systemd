%bcond_with bootstrap

# macros for sysvinit transition - should be equal to
# sysvinit %version-%release-plus-1
%define sysvinit_version 2.87
%define sysvinit_release %mkrel 23

%define libsystemd_major 0
%define libnss_major 2

%define libsystemd %mklibname %{name} %{libsystemd_major}
%define libsystemd_devel %mklibname %{name} -d

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
Version:	230
Release:	4
License:	GPLv2+
Group:		System/Configuration/Boot and Init
Url:		http://www.freedesktop.org/wiki/Software/systemd
Source0:	http://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.gz
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
# (tpg) EFI bootctl
Source21:	efi-loader.conf
Source22:	efi-omv.conf

### OMV patches###
# (tpg) add rpm macro to easy installation of user presets
Patch0:		systemd-230-add-userpreset-rpm-macro.patch
# from Mandriva
# disable coldplug for storage and device pci
#po 315
#Patch2:		udev-199-coldplug.patch
Patch5:		systemd-216-set-udev_log-to-err.patch
Patch8:		systemd-206-set-max-journal-size-to-150M.patch
#Patch9:		systemd-208-fix-race-condition-between-udev-and-vconsole.patch
Patch11:	systemd-220-silent-fsck-on-boot.patch
Patch14:	systemd-217-do-not-run-systemd-firstboot-in-containers.patch
Patch15:	1005-create-default-links-for-primary-cd_dvd-drive.patch
# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=1092
# keep this patch until upstream will fix it
Patch16:	systemd-219-always-restart-systemd-timedated.service.patch
Patch17:	0515-Add-path-to-locale-search.patch
Patch18:	0516-udev-silence-version-print.patch
Patch19:	0101-automount-handle-expire_tokens-when-the-mount-unit-c.patch
# (tpg) prolly this will be fixed dirrefently in next release
# https://bugzilla.redhat.com/show_bug.cgi?id=1141137
# For now best sollution is to enable UCH in kernel
# https://github.com/systemd/systemd/pull/350#issuecomment-137005614
# add to kernel boot parameter this systemd.unified_cgroup_hierarchy=1
# Patch19:	systemd-221-revert-wait_for_exit-true.patch

# UPSTREAM GIT PATCHES
# (tpg) fix build with kernel-headers >= 4.5
# https://github.com/systemd/systemd/issues/2864
#Patch100:	0000-shared-add-a-temporary-work-around-for-kernel-header.patch
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
BuildRequires:	elfutils-devel
BuildRequires:	pkgconfig(dbus-1) >= 1.10.0
BuildRequires:	pkgconfig(gee-0.8)
BuildRequires:	pkgconfig(glib-2.0)
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
BuildRequires:	pkgconfig(libiptc)
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(blkid) >= 2.27
BuildRequires:	usbutils >= 005-3
BuildRequires:	pciutils-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(liblz4)
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
BuildRequires:	pkgconfig(mount) >= 2.27
# make sure we have /etc/os-release available, required by --with-distro
BuildRequires:	distro-release-common >= 2012.0-0.4
%if !%{with bootstrap}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
%endif
Requires:	acl
Requires:	dbus >= 1.10.0
Requires(pre,post):	coreutils >= 8.23
Requires(post):	gawk
Requires(post):	awk
Requires(post):	grep
Requires(post):	awk
Requires(pre):	basesystem-minimal >= 1:3-0.1
Requires(pre):	util-linux >= 2.27
Requires(pre):	shadow >= 4.2.1-11
Requires(pre,post,postun):	setup >= 2.8.9
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
Requires:	%{libsystemd} = %{EVRD}
Requires:	%{libnss_myhostname} = %{EVRD}
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
Obsoletes:	python-%{name} < 223
Provides:	python-%{name} = 223
Obsoletes:	gummiboot
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

%package journal-gateway
Summary:	Gateway for serving journal events over the network using HTTP
Requires:	%{name} = %{EVRD}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Obsoletes:	systemd < 206-7

%description journal-gateway
Offers journal events over the network using HTTP.

%package -n %{libsystemd}
Summary:	Systemdlibrary package
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

%description -n	%{libsystemd}
This package provides the systemd shared library.

%package -n %{libsystemd_devel}
Summary:	Systemd library development files
Group:		Development/C
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

%description -n	%{libsystemd_devel}
Development files for the systemd shared library.

%package -n %{libnss_myhostname}
Summary:	Library for local system host name resolution
Group:		System/Libraries
Provides:	libnss_myhostname = %{EVRD}
Provides:	nss_myhostname = %{EVRD}
# (tpg) fix update from 2014.0
Provides:	nss_myhostname = 208-20
Obsoletes:	nss_myhostname < 208-20
Requires(post,preun):	bash
Requires(post,preun):	sed
Requires(post,preun):	glibc

%description -n %{libnss_myhostname}
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2).

%package -n %{libudev}
Summary:	Library for udev
Group:		System/Libraries
Obsoletes:	%{mklibname hal 1} <= 0.5.14-6

%description -n	%{libudev}
Library for udev.

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

%ifarch %{ix86}
# (tpg) remove -flto as on i586 it hangs boot
sed -i -e "s/-flto\]/-fno-lto\]/g" configure*
%endif

./autogen.sh

%build
%ifarch %{ix86}
# (tpg) since LLVM/clang-3.8.0 systemd hangs system
export CC=gcc
export CXX=g++
%endif

%serverbuild_hardened
%configure \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib} \
	--libexecdir=%{_prefix}/lib \
	--enable-compat-libs \
	--enable-bzip2 \
	--enable-lz4 \
	--without-kill-user-processes \
	--disable-static \
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
	--with-certificate-root="%{_sysconfdir}/pki" \
	--disable-kdbus \
	--with-ntp-servers="0.openmandriva.pool.ntp.org 1.openmandriva.pool.ntp.org 2.openmandriva.pool.ntp.org 3.openmandriva.pool.ntp.org" \
	--with-dns-servers="208.67.222.222 208.67.220.220"

%make

%install
%makeinstall_std

mkdir -p %{buildroot}{/bin,%{_sbindir}}

# (bor) create late shutdown and sleep directory
mkdir -p %{buildroot}%{systemd_libdir}/system-shutdown
mkdir -p %{buildroot}%{systemd_libdir}/system-sleep

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
mkdir -p %{buildroot}/sbin
ln -s ..%{systemd_libdir}/%{name} %{buildroot}/sbin/init
ln -s ..%{systemd_libdir}/%{name} %{buildroot}/bin/%{name}

# (tpg) install compat symlinks
for i in halt poweroff reboot; do
    ln -s /bin/systemctl %{buildroot}/bin/$i
done

for i in runlevel shutdown telinit; do
    ln -s ../bin/systemctl %{buildroot}/sbin/$i
done

ln -s /bin/loginctl %{buildroot}%{_bindir}/%{name}-loginctl

# (tpg) dracut needs this
ln -s /bin/systemctl %{buildroot}%{_bindir}/systemctl

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r %{buildroot}%{_sysconfdir}/%{name}/system/*.target.wants

# Make sure these directories are properly owned
mkdir -p %{buildroot}/%{systemd_libdir}/system/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/dbus.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/syslog.target.wants
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/system/getty.target.wants

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

# (bor) enable rpcbind.target by default so we have something to plug portmapper service into
ln -s ../rpcbind.target %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants

# (tpg) explicitly enable these services
ln -sf /lib/%{name}/system/%{name}-resolved.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/%{name}-resolved.service
ln -sf /lib/%{name}/system/%{name}-networkd.service %{buildroot}/%{systemd_libdir}/system/multi-user.target.wants/%{name}-networkd.service
ln -sf /lib/%{name}/system/%{name}-timesyncd.service %{buildroot}/%{systemd_libdir}/system/sysinit.target.wants/%{name}-timesyncd.service

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

# (tpg) install network file
install -m 0644 %{SOURCE17} %{buildroot}%{systemd_libdir}/network/
# (fedya) install wireless file
install -m 0644 %{SOURCE20} %{buildroot}%{systemd_libdir}/network/

# (tpg) install userspace presets
install -m 0644 %{SOURCE18} %{buildroot}%{_prefix}/lib/%{name}/user-preset/

# Install rsyslog fragment
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/rsyslog.d/

# (tpg) silent kernel messages
# print only KERN_ERR and more serious alerts
echo "kernel.printk = 3 3 3 3" >> %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) by default enable SysRq
sed -i -e 's/^#kernel.sysrq = 0/kernel.sysrq = 1/' %{buildroot}/usr/lib/sysctl.d/50-default.conf

# (tpg) use 100M as a default maximum value for journal logs
sed -i -e 's/^#SystemMaxUse=.*/SystemMaxUse=100M/' %{buildroot}%{_sysconfdir}/%{name}/journald.conf

%ifnarch %armx
install -m644 -D %{SOURCE21} %{buildroot}%{_datadir}/%{name}/bootctl/loader.conf
install -m644 -D %{SOURCE22} %{buildroot}%{_datadir}/%{name}/bootctl/omv.conf
%endif

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

ln -s ..%{systemd_libdir}/%{name}-udevd %{buildroot}/sbin/udevd
ln -s %{systemd_libdir}/%{name}-udevd %{buildroot}%{udev_libdir}/udevd

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
    systemctl stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :
fi

%post
/bin/systemd-firstboot --setup-machine-id
/bin/systemd-sysusers
/bin/systemd-machine-id-setup >/dev/null 2>&1 ||:
%{systemd_libdir}/systemd-random-seed save >/dev/null 2>&1 || :
/bin/systemctl daemon-reexec >/dev/null 2>&1 || :
/bin/systemctl start systemd-udevd.service >/dev/null 2>&1 || :
/bin/systemd-hwdb update >/dev/null 2>&1 || :
/bin/journalctl --update-catalog >/dev/null 2>&1 || :

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

# Remove spurious /etc/fstab entries from very old installations
if [ -e /etc/fstab ]; then
    grep -v -E -q '^(devpts|tmpfs|sysfs|proc)' /etc/fstab || \
	sed -i.rpm.bak -r '/^devpts\s+\/dev\/pts\s+devpts\s+defaults\s+/d; /^tmpfs\s+\/dev\/shm\s+tmpfs\s+defaults\s+/d; /^sysfs\s+\/sys\s+sysfs\s+defaults\s+/d; /^proc\s+\/proc\s+proc\s+defaults\s+/d' /etc/fstab || :
fi

# (tpg) create resolv.conf based on systemd
if [ $1 -ge 1 ]; then
    if [ ! -e /run/systemd/resolve/resolv.conf ]; then
	mkdir -p /run/systemd/resolve
	echo -e "nameserver 208.67.222.222\nnameserver 208.67.220.220\n" > /run/systemd/resolve/resolv.conf
    fi
fi

# (tpg) link to resolv.conf from systemd
if [ $1 -eq 1 ]; then
    if [ -e /etc/resolv.conf ]; then
	rm -f /etc/resolv.conf
    fi
    ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
fi

# (tpg) on update always set to systemd resolv.conf
if [ $1 -ge 2 ]; then
    if [ -L /etc/resolv.conf ] && [ "$(readlink /etc/resolv.conf)" != "../run/systemd/resolve/resolv.conf" ]; then
	rm -f /etc/resolv.conf
	ln -sf ../run/systemd/resolve/resolv.conf /etc/resolv.conf
    fi

    /bin/systemctl restart systemd-resolved.service 2>&1 || :
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

%triggerposttransin -- /lib/udev/hwdb.d/*.hwdb
/bin/systemd-hwdb update

%triggerposttransun -- /lib/udev/hwdb.d/*.hwdb
/bin/systemd-hwdb update

%triggerposttransin -- %{_prefix}/lib/sysusers.d/*.conf
/bin/systemd-sysusers

%triggerposttransun -- %{_prefix}/lib/sysusers.d/*.conf
/bin/systemd-sysusers

%triggerposttransin -- %{_prefix}/lib/systemd/catalog/*.catalog
/bin/journalctl --update-catalog

%triggerposttransun -- %{_prefix}/lib/systemd/catalog/*.catalog
/bin/journalctl --update-catalog

%post -n %{libnss_myhostname}
# sed-fu to remove mymachines from passwd and group lines of /etc/nsswitch.conf
# https://bugzilla.redhat.com/show_bug.cgi?id=1284325
# To avoid the removal, e.g. add a space at the end of the line.
if [ -f /etc/nsswitch.conf ] ; then
    grep -E -q '^(passwd|group):.* mymachines$' /etc/nsswitch.conf &&
    sed -i.bak -r -e '
	s/^(passwd:.*) mymachines$/\1/;
	s/^(group:.*) mymachines$/\1/;
	' /etc/nsswitch.conf >/dev/null 2>&1 || :
fi

%preun -n %{libnss_myhostname}
if [ -f /etc/nsswitch.conf ] ; then
    sed -i.bak -e '
	/^hosts:/ !b
	s/[[:blank:]]\+myhostname\>//
	' /etc/nsswitch.conf >/dev/null 2>&1 || :

    sed -i.bak -e '
	/^hosts:/ !b
	s/[[:blank:]]\+mymachines\>//
	' /etc/nsswitch.conf >/dev/null 2>&1 || :
fi

%pre journal-gateway
%_pre_groupadd systemd-journal-gateway systemd-journal-gateway
%_pre_useradd systemd-journal-gateway %{_var}/log/journal /sbin/nologin
%_pre_groupadd systemd-journal-remote systemd-journal-remote
%_pre_useradd systemd-journal-remote %{_var}/log/journal/remote /sbin/nologin
%_pre_groupadd systemd-journal-upload systemd-journal-upload
%_pre_useradd systemd-journal-upload %{_var}/log/journal/upload /sbin/nologin

%files -f %{name}.lang
%doc %{_docdir}/%{name}
%dir /lib/firmware
%dir /lib/firmware/updates
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%dir %{_datadir}/factory
%dir %{_datadir}/factory/etc
%dir %{_datadir}/factory/etc/pam.d
%dir %{_datadir}/%{name}
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%dir %{_prefix}/lib/%{name}
%ifnarch %armx
%dir %{_prefix}/lib/%{name}/boot
%dir %{_prefix}/lib/%{name}/boot/efi
%dir %{_datadir}/%{name}/bootctl
%endif
%dir %{_prefix}/lib/%{name}/catalog
%dir %{_prefix}/lib/%{name}/system-generators
%dir %{_prefix}/lib/%{name}/user
%dir %{_prefix}/lib/%{name}/user-preset
%dir %{_prefix}/lib/%{name}/user-generators
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
%dir %{_sysconfdir}/%{name}/network
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
%dir %{udev_libdir}
%dir %{udev_libdir}/hwdb.d
%dir %{udev_rules_dir}
%exclude %{_mandir}/man8/libnss_myhostname.so.2.8.*
%exclude %{_mandir}/man8/libnss_mymachines.so.2.8.*
%exclude %{_mandir}/man8/nss-myhostname.8.*
%exclude %{_mandir}/man8/nss-mymachines.8.*
%exclude %{_mandir}/man8/%{name}-journal-gatewayd.8.*
%exclude %{_mandir}/man8/%{name}-journal-gatewayd.service.8.*
%exclude %{_mandir}/man8/%{name}-journal-gatewayd.socket.8.*
%exclude %{_mandir}/man8/%{name}-journal-remote.8.*
%exclude %{_mandir}/man8/%{name}-journal-upload.8.*
%exclude %{_prefix}/lib/tmpfiles.d/%{name}-remote.conf
%exclude %{systemd_libdir}/system/%{name}-journal-gatewayd.service
%exclude %{systemd_libdir}/system/%{name}-journal-gatewayd.socket
%exclude %{systemd_libdir}/system/%{name}-journal-remote.service
%exclude %{systemd_libdir}/system/%{name}-journal-remote.socket
%exclude %{systemd_libdir}/system/%{name}-journal-upload.service
%exclude %{systemd_libdir}/%{name}-journal-gatewayd
%exclude %{systemd_libdir}/%{name}-journal-remote
%exclude %{systemd_libdir}/%{name}-journal-upload
%exclude %config(noreplace) %{_prefix}/lib/sysusers.d/%{name}-remote.conf
%exclude %config(noreplace) %{_sysconfdir}/%{name}/journal-remote.conf
%exclude %config(noreplace) %{_sysconfdir}/%{name}/journal-upload.conf
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
/bin/%{name}
/bin/%{name}-ask-password
/bin/%{name}-escape
/bin/%{name}-firstboot
/bin/%{name}-hwdb
/bin/%{name}-inhibit
/bin/%{name}-machine-id-setup
/bin/%{name}-notify
/bin/%{name}-sysusers
/bin/%{name}-tmpfiles
/bin/%{name}-tty-ask-password-agent
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
%{_bindir}/%{name}-*
%{_bindir}/timedatectl
%{_datadir}/bash-completion/completions/*
%{_datadir}/dbus-1/*services/*.service
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/%{name}/kbd-model-map
%{_datadir}/%{name}/language-fallback-map
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
%{_prefix}/lib/%{name}/boot/efi/*.efi
%{_prefix}/lib/%{name}/boot/efi/*.stub
%{_datadir}/%{name}/bootctl/*.conf
%endif
%{_prefix}/lib/%{name}/catalog/*.catalog
%{_prefix}/lib/%{name}/user-generators/%{name}-dbus1-generator
%{_prefix}/lib/%{name}/user-preset/*.preset
%{_prefix}/lib/%{name}/user/*.service
%{_prefix}/lib/%{name}/user/*.target
%{_prefix}/lib/tmpfiles.d/*.conf
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/rpm/macros.d/systemd.macros
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/xdg/%{name}
%{systemd_libdir}/*-generators/*
%{systemd_libdir}/import-pubring.gpg
%{systemd_libdir}/network/80-container-host0.network
%{systemd_libdir}/network/80-container-ve.network
%{systemd_libdir}/network/80-container-vz.network
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

%{udev_libdir}/hwdb.d/*.hwdb
%{udev_rules_dir}/*.rules
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal
%attr(0755,root,root) /sbin/udevadm
%attr(0755,root,root) /sbin/udevd
%attr(0755,root,root) %{_bindir}/udevadm
%attr(0755,root,root) %{_sbindir}/udevadm
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
%config(noreplace) %{_sysconfdir}/pam.d/%{name}-user
%config(noreplace) %{_sysconfdir}/rsyslog.d/listen.conf
%config(noreplace) %{_sysconfdir}/sysconfig/udev
%config(noreplace) %{_sysconfdir}/sysconfig/udev_net
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/udev/*.conf

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
%{_prefix}/lib/tmpfiles.d/%{name}-remote.conf
%{_mandir}/man8/%{name}-journal-gatewayd.8.*
%{_mandir}/man8/%{name}-journal-upload.8.*
%{_mandir}/man8/%{name}-journal-remote.8.*
%{_mandir}/man8/%{name}-journal-gatewayd.service.8.*
%{_mandir}/man8/%{name}-journal-gatewayd.socket.8.*
%{_datadir}/%{name}/gatewayd/browse.html

%files -n %{libnss_myhostname}
%{_libdir}/libnss_myhostname.so.%{libnss_major}*
%{_libdir}/libnss_mymachines.so.%{libnss_major}
%{_libdir}/libnss_resolve.so.%{libnss_major}
%{_mandir}/man8/libnss_myhostname.so*.8*
%{_mandir}/man8/libnss_mymachines.so*.8*
%{_mandir}/man8/nss-myhostname.8*
%{_mandir}/man8/nss-mymachines.8*

%files -n %{libsystemd}
/%{_lib}/libsystemd.so.%{libsystemd_major}*

%files -n %{libsystemd_devel}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/_sd-common.h
%{_includedir}/%{name}/sd-bus-protocol.h
%{_includedir}/%{name}/sd-bus-vtable.h
%{_includedir}/%{name}/sd-bus.h
%{_includedir}/%{name}/sd-event.h
%{_includedir}/%{name}/sd-id128.h
%{_includedir}/%{name}/sd-journal.h
%{_includedir}/%{name}/sd-login.h
%{_includedir}/%{name}/sd-messages.h
%{_includedir}/%{name}/sd-daemon.h
%{_libdir}/lib%{name}.so
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/lib%{name}.pc

%files -n %{libudev}
/%{_lib}/libudev.so.%{udev_major}*

%files -n %{libudev_devel}
%{_libdir}/libudev.so
%{_libdir}/pkgconfig/libudev.pc
%{_datadir}/pkgconfig/udev.pc
%{_includedir}/libudev.h
