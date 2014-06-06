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
%define libdaemon_devel %mklibname systemd-daemon -d

%define liblogin %mklibname systemd-login %{liblogin_major}
%define liblogin_devel %mklibname systemd-login -d

%define libjournal %mklibname systemd-journal %{libjournal_major}
%define libjournal_devel %mklibname systemd-journal -d

%define libid128 %mklibname systemd-id128 %{libid128_major}
%define libid128_devel %mklibname systemd-id128 -d

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
Version:	208
Release:	19.1
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
Source15:	enable-numlock.conf

Source16:	systemd.rpmlintrc

### OMV patches###
# from Mandriva
# disable coldplug for storage and device pci
#po 315
#Patch2:		udev-199-coldplug.patch
Patch3:		systemd-205-uclibc.patch
# We need a static libudev.a for the uClibc build because lvm2 requires it.
# Put back support for building it.
Patch4:		systemd-205-static.patch
Patch5:		systemd-186-set-udev_log-to-err.patch
# uClibc lacks secure_getenv(), DO NOT REMOVE!
Patch6:		systemd-196-support-build-without-secure_getenv.patch
Patch7:		systemd-191-uclibc-no-mkostemp.patch
Patch8:		systemd-206-set-max-journal-size-to-150M.patch
Patch9:		systemd-208-fix-race-condition-between-udev-and-vconsole.patch

#Upstream patchset
Patch100:	0100-fix-lingering-references-to-var-lib-backlight-random.patch
Patch101:	0101-acpi-make-sure-we-never-free-an-uninitialized-pointe.patch
Patch102:	0102-systemctl-fix-name-mangling-for-sysv-units.patch
Patch103:	0103-cryptsetup-fix-OOM-handling-when-parsing-mount-optio.patch
Patch104:	0104-journald-add-missing-error-check.patch
Patch105:	0105-bus-fix-potentially-uninitialized-memory-access.patch
Patch106:	0106-dbus-fix-return-value-of-dispatch_rqueue.patch
Patch107:	0107-modules-load-fix-error-handling.patch
Patch108:	0108-efi-never-call-qsort-on-potentially-NULL-arrays.patch
Patch109:	0109-strv-don-t-access-potentially-NULL-string-arrays.patch
Patch110:	0110-mkdir-pass-a-proper-function-pointer-to-mkdir_safe_i.patch
Patch111:	0111-tmpfiles.d-include-setgid-perms-for-run-log-journal.patch
Patch112:	0112-execute.c-always-set-SHELL.patch
Patch113:	0113-man-Improve-the-description-of-parameter-X-in-tmpfil.patch
Patch114:	0114-execute-more-debugging-messages.patch
Patch115:	0115-gpt-auto-generator-exit-immediately-if-in-container.patch
Patch116:	0116-systemd-order-remote-mounts-from-mountinfo-before-re.patch
Patch117:	0117-manager-when-verifying-whether-clients-may-change-en.patch
Patch118:	0118-logind-fix-bus-introspection-data-for-TakeControl.patch
Patch119:	0119-mount-check-for-NULL-before-reading-pm-what.patch
Patch120:	0120-core-do-not-add-what-to-RequiresMountsFor-for-networ.patch
Patch121:	0121-utf8-fix-utf8_is_printable.patch
Patch122:	0122-shared-util-fix-off-by-one-error-in-tag_to_udev_node.patch
Patch123:	0123-systemd-serialize-deserialize-forbid_restart-value.patch
Patch124:	0124-core-unify-the-way-we-denote-serialization-attribute.patch
Patch125:	0125-journald-fix-minor-memory-leak.patch
Patch126:	0126-keymap-Fix-Samsung-900X-34-C.patch
Patch127:	0127-do-not-accept-garbage-from-acpi-firmware-performance.patch
Patch128:	0128-journald-remove-rotated-file-from-hashmap-when-rotat.patch
Patch129:	0129-login-fix-invalid-free-in-sd_session_get_vt.patch
Patch130:	0130-login-make-sd_session_get_vt-actually-work.patch
Patch131:	0131-udevadm.xml-document-resolve-names-option-for-test.patch
Patch132:	0132-Never-call-qsort-on-potentially-NULL-arrays.patch
Patch133:	0133-dbus-common-avoid-leak-in-error-path.patch
Patch134:	0134-drop-ins-check-return-value.patch
Patch135:	0135-Make-sure-that-we-don-t-dereference-NULL.patch
Patch136:	0136-gitignore-ignore-clang-analyze-output.patch
Patch137:	0137-man-add-more-markup-to-udevadm-8.patch
Patch138:	0138-shared-util-Fix-glob_extend-argument.patch
Patch139:	0139-Fix-bad-assert-in-show_pid_array.patch
Patch140:	0140-Fix-for-SIGSEGV-in-systemd-bootchart-on-short-living.patch
Patch141:	0141-man-document-the-b-special-boot-option.patch
Patch142:	0142-logind-allow-unprivileged-session-device-access.patch
Patch143:	0143-rules-expose-loop-block-devices-to-systemd.patch
Patch144:	0144-rules-don-t-limit-some-of-the-rules-to-the-add-actio.patch
Patch145:	0145-tmpfiles-log-unaccessible-FUSE-mount-points-only-as-.patch
Patch146:	0146-hwdb-update.patch
Patch147:	0147-rules-remove-pointless-MODE-settings.patch
Patch148:	0148-analyze-set-white-backgound.patch
Patch149:	0149-shell-completion-dump-has-moved-to-systemd-analyze.patch
Patch150:	0150-systemd-use-unit-name-in-PrivateTmp-directories.patch
Patch151:	0151-catalog-remove-links-to-non-existent-wiki-pages.patch
Patch152:	0152-journalctl-add-list-boots-to-show-boot-IDs-and-times.patch
Patch153:	0153-udev-builtin-path_id-add-support-for-bcma-bus.patch
Patch154:	0154-udev-ata_id-log-faling-ioctls-as-debug.patch
Patch155:	0155-libudev-default-log_priority-to-INFO.patch
Patch156:	0156-nspawn-only-pass-in-slice-setting-if-it-is-set.patch
Patch157:	0157-zsh-completion-add-systemd-run.patch
Patch158:	0158-man-explain-NAME-in-systemctl-man-page.patch
Patch159:	0159-virt-move-caching-of-virtualization-check-results-in.patch
Patch160:	0160-systemctl-fix-typo-in-help-text.patch
Patch161:	0161-analyze-plot-place-the-text-on-the-side-with-most-sp.patch
Patch162:	0162-detect_virtualization-returns-NULL-pass-empty-string.patch
Patch163:	0163-rules-load-path_id-on-DRM-devices.patch
Patch164:	0164-rules-simply-60-drm.rules.patch
Patch165:	0165-udev-builtin-keyboard-Fix-large-scan-codes-on-32-bit.patch
Patch166:	0166-nspawn-log-out-of-memory-errors.patch
Patch167:	0167-Configurable-Timeouts-Restarts-default-values.patch
Patch168:	0168-man-fix-typo.patch
Patch169:	0169-man-do-not-use-term-in-para.patch
Patch170:	0170-cgroup-run-PID-1-in-the-root-cgroup.patch
Patch171:	0171-shutdown-trim-the-cgroup-tree-on-loop-iteration.patch
Patch172:	0172-nspawn-split-out-pty-forwaring-logic-into-ptyfwd.c.patch
Patch173:	0173-nspawn-explicitly-terminate-machines-when-we-exit-ns.patch
Patch174:	0174-run-support-system-to-match-other-commands-even-if-r.patch
Patch175:	0175-acpi-fpdt-break-on-zero-or-negative-length-read.patch
Patch176:	0176-man-add-rationale-into-systemd-halt-8.patch
Patch177:	0177-systemd-python-convert-keyword-value-to-string.patch
Patch178:	0178-systemctl-make-LOAD-column-width-dynamic.patch
Patch179:	0179-Make-hibernation-test-work-for-swap-files.patch
Patch180:	0180-man-add-docs-for-sd_is_special-and-some-man-page-sym.patch
Patch181:	0181-systemctl-return-r-instead-of-always-returning-0.patch
Patch182:	0182-journal-fix-minor-memory-leak.patch
Patch183:	0183-manager-configurable-StartLimit-default-values.patch
Patch184:	0184-man-units-fix-installation-of-systemd-nspawn-.servic.patch
Patch185:	0185-systemd-fix-memory-leak-in-cgroup-code.patch
Patch186:	0186-button-don-t-exit-if-we-cannot-handle-a-button-press.patch
Patch187:	0187-timer-properly-format-relative-timestamps-in-the-fut.patch
Patch188:	0188-timer-consider-usec_t-1-an-invalid-timestamp.patch
Patch189:	0189-udev-usb_id-remove-obsoleted-bInterfaceSubClass-5-ma.patch
Patch190:	0190-Add-support-for-saving-restoring-keyboard-backlights.patch
Patch191:	0191-static-nodes-don-t-call-mkdir.patch
Patch192:	0192-Fix-kmod-error-message-to-have-correct-version-requi.patch
Patch193:	0193-systemd-python-fix-booted-and-add-two-functions-to-d.patch
Patch194:	0194-activate-mention-E-in-the-help-text.patch
Patch195:	0195-activate-fix-crash-when-s-is-passed.patch
Patch196:	0196-journal-timestamp-support-on-console-messages.patch
Patch197:	0197-man-add-bootctl-8.patch
Patch198:	0198-zsh-completion-add-bootctl.patch
Patch199:	0199-Resolve-dev-console-to-the-active-tty-instead-of-jus.patch
Patch200:	0200-Only-disable-output-on-console-during-boot-if-needed.patch
Patch201:	0201-Fix-possible-lack-of-status-messages-on-shutdown-reb.patch
Patch202:	0202-fsck-modernization.patch
Patch203:	0203-Introduce-udev-object-cleanup-functions.patch
Patch204:	0204-util-allow-trailing-semicolons-on-define_trivial_cle.patch
Patch205:	0205-fsck-fstab-generator-be-lenient-about-missing-fsck.-.patch
Patch206:	0206-fstab-generator-use-RequiresOverridable-for-fsck-uni.patch
Patch207:	0207-bash-completion-journalctl-file.patch
Patch208:	0208-random-seed-improve-debugging-messages-a-bit.patch
Patch209:	0209-Fix-RemainAfterExit-services-keeping-a-hold-on-conso.patch
Patch210:	0210-tmpfiles-adjust-excludes-for-the-new-per-service-pri.patch
Patch211:	0211-core-socket-fix-SO_REUSEPORT.patch
Patch212:	0212-localed-match-converted-keymaps-before-legacy.patch
Patch213:	0213-keymap-Add-Toshiba-Satellite-U940.patch
Patch214:	0214-calendar-support-yearly-and-annually-names-the-same-.patch
Patch215:	0215-hashmap-be-a-bit-more-conservative-with-pre-allocati.patch
Patch216:	0216-manager-don-t-do-plymouth-in-a-container.patch
Patch217:	0217-nspawn-add-new-drop-capability-switch.patch
Patch218:	0218-valgrind-make-running-PID-1-in-valgrind-useful.patch
Patch219:	0219-efi-boot-generator-don-t-mount-boot-eagerly.patch
Patch220:	0220-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch221:	0221-journal-when-appending-to-journal-file-allocate-larg.patch
Patch222:	0222-journal-make-table-const.patch
Patch223:	0223-journald-keep-statistics-on-how-of-we-hit-miss-the-m.patch
Patch224:	0224-journal-optimize-bisection-logic-a-bit-by-caching-th.patch
Patch225:	0225-journal-fix-iteration-when-we-go-backwards-from-the-.patch
Patch226:	0226-journal-allow-journal_file_copy_entry-to-work-on-non.patch
Patch227:	0227-journal-simplify-pre-allocation-logic.patch
Patch228:	0228-journald-mention-how-long-we-needed-to-flush-to-var-.patch
Patch229:	0229-automount-log-info-about-triggering-process.patch
Patch230:	0230-virt-split-detect_vm-into-separate-functions.patch
Patch231:	0231-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch232:	0232-sysfs-show.c-return-negative-error.patch
Patch233:	0233-util.c-check-if-return-value-from-ttyname_r-is-0-ins.patch
Patch234:	0234-docs-remove-unneeded-the-s-in-gudev-docs.patch
Patch235:	0235-man-explicitly-say-when-multiple-units-can-be-specif.patch
Patch236:	0236-systemd-treat-reload-failure-as-failure.patch
Patch237:	0237-journal-fail-silently-in-sd_j_sendv-if-journal-is-un.patch
Patch238:	0238-systemd-add-a-start-job-for-all-units-specified-with.patch
Patch239:	0239-core-device-ignore-SYSTEMD_WANTS-in-user-mode.patch
Patch240:	0240-Fix-memory-leak-in-stdout-journal-streams.patch
Patch241:	0241-man-document-is-enabled-output.patch
Patch242:	0242-hostnamed-avoid-using-NULL-in-error-path.patch
Patch243:	0243-logind-use-correct-who-enum-values-with-KillUnit.patch
Patch244:	0244-Revert-systemd-add-a-start-job-for-all-units-specifi.patch
Patch245:	0245-core-do-not-segfault-if-swap-activity-happens-when-p.patch
Patch246:	0246-kernel-install-add-h-help.patch
Patch247:	0247-kernel-install-fix-help-output.patch
Patch248:	0248-man-improve-wording-and-comma-usage-in-systemd.journ.patch
Patch249:	0249-drop-several-entries-from-kbd-model-map-whose-kbd-la.patch
Patch250:	0250-correct-name-of-Tajik-kbd-layout-in-kbd-model-map.patch
Patch251:	0251-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch252:	0252-Ensure-unit-is-journaled-for-short-lived-or-oneshot-.patch
Patch253:	0253-libudev-hwdb-use-libudev-not-systemd-logging.patch
Patch254:	0254-core-manager-remove-infinite-loop.patch
Patch255:	0255-util-check-for-overflow-in-greedy_realloc.patch
Patch256:	0256-journald-use-a-bit-more-cleanup-magic.patch
Patch257:	0257-journald-malloc-less-when-streaming-messages.patch
Patch258:	0258-activate-clean-up-inherited-descriptors.patch
Patch259:	0259-man-explain-in-more-detail-how-SYSTEMD_READY-influen.patch
Patch260:	0260-units-don-t-run-readahead-done-timers-in-containers.patch
Patch261:	0261-test-fileio-replace-mktemp-with-mkstemp-to-avoid-war.patch
Patch262:	0262-journal-pipe-journalctl-help-output-into-a-pager.patch
Patch263:	0263-nspawn-complain-and-continue-if-machine-has-same-id.patch
Patch264:	0264-man-beef-up-ExecStart-description.patch
Patch265:	0265-man-remove-advice-to-avoid-setting-the-same-var-more.patch
Patch266:	0266-systemctl-add-the-plain-option-to-the-help-message.patch
Patch267:	0267-Fix-a-few-resource-leaks-in-error-paths.patch
Patch268:	0268-Fix-a-few-signed-unsigned-format-string-issues.patch
Patch269:	0269-util-try-harder-to-increase-the-send-recv-buffers-of.patch
Patch270:	0270-execute-also-set-SO_SNDBUF-when-spawning-a-service-w.patch
Patch271:	0271-journal-file-protect-against-alloca-0.patch
Patch272:	0272-man-describe-journalctl-show-cursor.patch
Patch273:	0273-journal-fix-against-theoretical-undefined-behavior.patch
Patch274:	0274-journald-downgrade-warning-message-when-dev-kmsg-doe.patch
Patch275:	0275-journal-file.c-remove-redundant-assignment-of-variab.patch
Patch276:	0276-login-Don-t-stop-a-running-user-manager-from-garbage.patch
Patch277:	0277-libudev-devices-received-from-udev-are-always-initia.patch
Patch278:	0278-log-don-t-reopen-dev-console-each-time-we-call-log_o.patch
Patch279:	0279-log-when-we-log-to-dev-console-and-got-disconnected-.patch
Patch280:	0280-loginctl-when-showing-device-tree-of-seats-with-no-d.patch
Patch281:	0281-man-be-more-explicit-about-option-arguments-that-tak.patch
Patch282:	0282-man-add-DOI-for-refereed-article-on-Forward-Secure-S.patch
Patch283:	0283-journalctl-zsh-completion-fix-several-issues-in-help.patch
Patch284:	0284-keymap-Refactor-Acer-tables.patch
Patch285:	0285-logging-reduce-send-timeout-to-something-more-sensib.patch
Patch286:	0286-DEFAULT_PATH_SPLIT_USR-macro.patch
Patch287:	0287-fstab-generator-Do-not-try-to-fsck-non-devices.patch
Patch288:	0288-logind-remove-dead-variable.patch
Patch289:	0289-hwdb-update.patch
Patch290:	0290-delta-replace-readdir_r-with-readdir.patch
Patch291:	0291-delta-fix-delta-for-drop-ins.patch
Patch292:	0292-delta-if-prefix-is-specified-only-show-overrides-the.patch
Patch293:	0293-log-log_error-and-friends-add-a-newline-after-each-l.patch
Patch294:	0294-man-units-tmpfiles.d-5-cleanup.patch
Patch295:	0295-tmpfiles-introduce-the-concept-of-unsafe-operations.patch
Patch296:	0296-sleep-config-fix-useless-check-for-swapfile-type.patch
Patch297:	0297-journalctl-make-sure-b-foobar-cannot-be-misunderstoo.patch
Patch298:	0298-man-resolve-word-omissions.patch
Patch299:	0299-man-improvements-to-comma-placement.patch
Patch300:	0300-man-grammar-and-wording-improvements.patch
Patch301:	0301-man-document-fail-nofail-auto-noauto.patch
Patch302:	0302-man-fix-description-of-is-enabled-returned-value.patch
Patch303:	0303-man-fix-Type-reference.patch
Patch304:	0304-man-fix-Type-reference-v2.patch
Patch305:	0305-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch306:	0306-man-add-a-note-about-propagating-signals.patch
Patch307:	0307-man-include-autoconf-snippet-in-daemon-7.patch
Patch308:	0308-systemd-python-fix-setting-of-exception-codes.patch
Patch309:	0309-systemd-python-fix-listen_fds-under-Python-2.patch
Patch310:	0310-man-expand-on-some-more-subtle-points-in-systemd.soc.patch
Patch311:	0311-tmpfiles-rename-unsafe-to-boot.patch
Patch312:	0312-sleep-config-Dereference-pointer-before-check-for-NU.patch
Patch313:	0313-sleep-config-fix-double-free.patch
Patch314:	0314-rules-drivers-do-not-reset-RUN-list.patch
Patch315:	0315-core-manager-print-info-about-interesting-signals.patch
Patch316:	0316-core-service-check-if-mainpid-matches-only-if-it-is-.patch
Patch317:	0317-man-typo-fix.patch
Patch318:	0318-swap-remove-if-else-with-the-same-data-path.patch
Patch319:	0319-hwdb-update.patch
Patch320:	0320-journal-Add-missing-byte-order-conversions.patch
Patch321:	0321-hwdb-change-key-mappings-for-Samsung-90X3A.patch
Patch322:	0322-hwdb-add-Samsung-700G.patch
Patch323:	0323-hwdb-remove-duplicate-entry-for-Samsung-700Z.patch
Patch324:	0324-hwdb-fix-match-for-Thinkpad-X201-tablet.patch
Patch325:	0325-keymap-Recognize-different-Toshiba-Satellite-capital.patch
Patch326:	0326-sleep.c-fix-typo.patch
Patch327:	0327-delta-ensure-that-d_type-will-be-set-on-every-fs.patch
Patch328:	0328-tmpfiles-don-t-allow-label_fix-to-print-ENOENT-when-.patch
Patch329:	0329-man-mention-which-variables-will-be-expanded-in-Exec.patch
Patch330:	0330-hwdb-Add-support-for-Toshiba-Satellite-P75-A7200-key.patch
Patch331:	0331-journal-fix-access-to-munmapped-memory-in-sd_journal.patch
Patch332:	0332-gpt-auto-generator-skip-nonexistent-devices.patch
Patch333:	0333-gpt-auto-generator-use-EBADSLT-code-when-unable-to-d.patch
Patch334:	0334-journald-do-not-free-space-when-disk-space-runs-low.patch
Patch335:	0335-man-add-busctl-1.patch
Patch336:	0336-journalctl-flip-to-full-by-default.patch
Patch337:	0337-coredumpctl-in-case-of-error-free-pattern-after-prin.patch
Patch338:	0338-shell-completion-remove-load-from-systemctl.patch
Patch339:	0339-units-drop-Install-section-from-multi-user.target-an.patch
Patch340:	0340-systemctl-skip-native-unit-file-handling-if-sysv-fil.patch
Patch341:	0341-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch342:	0342-udev-static_node-do-not-exit-rule-after-first-static.patch
Patch343:	0343-cryptsetup-Support-key-slot-option.patch
Patch344:	0344-pam_systemd-Ignore-vtnr-when-seat-seat0.patch
Patch345:	0345-keymap-Add-HP-Chromebook-14-Falco.patch
Patch346:	0346-keymap-Add-release-quirk-for-Acer-AOA-switchvideomod.patch
Patch347:	0347-keymap-Add-Sony-Vaio-VGN-FW250.patch
Patch348:	0348-keymap-Add-Toshiba-EQUIUM.patch
Patch349:	0349-tmpfiles-fix-memory-leak-of-exclude_prefixes.patch
Patch350:	0350-analyze-fix-plot-issues-when-using-gummiboot.patch
Patch351:	0351-udev-add-zram-to-the-list-of-devices-inappropriate-f.patch
Patch352:	0352-bash-completion-fix-completion-of-complete-verbs.patch
Patch353:	0353-shell-completion-fix-completion-of-localectl-set-loc.patch
Patch354:	0354-zsh-completions-kernel-install-only-show-existing-ke.patch
Patch355:	0355-core-fix-crashes-if-locale.conf-contains-invalid-utf.patch
Patch356:	0356-core-do-not-print-invalid-utf-8-in-error-messages.patch
Patch357:	0357-cryptsetup-generator-auto-add-deps-for-device-as-pas.patch
Patch358:	0358-man-fix-reference-in-systemd-inhibit-1.patch
Patch359:	0359-man-fix-another-reference-in-systemd-inhibit-1.patch
Patch360:	0360-fstab-generator-Create-fsck-root-symlink-with-correc.patch
Patch361:	0361-efi-fix-Undefined-reference-efi_loader_get_boot_usec.patch
Patch362:	0362-core-make-StopWhenUnneeded-work-in-conjunction-with-.patch
Patch363:	0363-man-always-place-programlisting-and-programlisting-i.patch
Patch364:	0364-Temporary-work-around-for-slow-shutdown-due-to-unter.patch
Patch365:	0365-pam-module-fix-warning-about-ignoring-vtnr.patch
Patch366:	0366-pam_systemd-do-not-set-XDG_RUNTIME_DIR-if-the-sessio.patch
Patch367:	0367-core-do-not-segfault-if-proc-swaps-cannot-be-opened.patch
Patch368:	0368-Revert-login-Don-t-stop-a-running-user-manager-from-.patch
Patch369:	0369-Revert-journalctl-flip-to-full-by-default.patch
Patch370:	0370-util-fix-handling-of-trailing-whitespace-in-split_qu.patch
Patch371:	0371-udev-net_id-Introduce-predictable-network-names-for-.patch
Patch372:	0372-utils-silence-the-compiler-warning.patch
Patch373:	0373-fix-SELinux-check-for-transient-units.patch
Patch374:	0374-s390-getty-generator-initialize-essential-system-ter.patch
Patch375:	0375-pam-use-correct-log-level.patch
Patch376:	0376-nspawn-if-we-don-t-find-bash-try-sh.patch
Patch377:	0377-units-systemd-logind-fails-hard-without-dbus.patch
Patch378:	0378-man-fix-grammatical-errors-and-other-formatting-issu.patch
Patch379:	0379-man-replace-STDOUT-with-standard-output-etc.patch
Patch380:	0380-man-use-spaces-instead-of-tabs.patch
Patch381:	0381-macro-add-a-macro-to-test-whether-a-value-is-in-a-sp.patch
Patch382:	0382-core-fix-property-changes-in-transient-units.patch
Patch383:	0383-core-more-exact-test-on-the-procfs-special-string-de.patch
Patch384:	0384-doc-update-punctuation.patch
Patch385:	0385-doc-resolve-missing-extraneous-words-or-inappropriat.patch
Patch386:	0386-doc-choose-different-words-to-improve-clarity.patch
Patch387:	0387-doc-properly-use-XML-entities.patch
Patch388:	0388-man-machinectl-there-is-no-command-kill-machine.patch
Patch389:	0389-load-modules-properly-return-a-failing-error-code-if.patch
Patch390:	0390-machinectl-add-bash-completion.patch
Patch391:	0391-delta-add-bash-completion.patch
Patch392:	0392-man-document-MAINPID.patch
Patch393:	0393-man-busctl-typo-fix.patch
Patch394:	0394-journal-don-t-clobber-return-parameters-of-sd_journa.patch
Patch395:	0395-udev-make-sure-we-always-return-a-valid-error-code-i.patch
Patch396:	0396-bootctl-add-bash-completion.patch
Patch397:	0397-selinux-Don-t-attempt-to-load-policy-in-initramfs-if.patch
Patch398:	0398-man-there-is-no-ExecStopPre-for-service-units.patch
Patch399:	0399-man-document-that-per-interface-sysctl-variables-are.patch
Patch400:	0400-journal-downgrade-vaccuum-message-to-debug-level.patch
Patch401:	0401-core-gc-half-created-stub-units.patch
Patch402:	0402-getty-generator-verify-ttys-before-we-make-use-of-th.patch
Patch403:	0403-units-serial-getty-.service-add-Install-section.patch
Patch404:	0404-README-document-that-var-run-must-be-a-symlink-run.patch
Patch405:	0405-Use-var-run-dbus-system_bus_socket-for-the-D-Bus-soc.patch
Patch406:	0406-mount-don-t-send-out-PropertiesChanged-message-if-ac.patch
Patch407:	0407-mount-don-t-fire-PropertiesChanged-signals-for-mount.patch
Patch408:	0408-logs-show-fix-corrupt-output-with-empty-messages.patch
Patch409:	0409-journalctl-refuse-extra-arguments-with-verify-and-si.patch
Patch410:	0410-cdrom_id-use-the-old-MMC-fallback.patch
Patch411:	0411-udev-rules-setup-tty-permissions-and-group-for-sclp_.patch
Patch412:	0412-bash-add-completion-for-systemd-nspawn.patch
Patch413:	0413-add-bash-completion-for-systemd-cgls.patch
Patch414:	0414-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch415:	0415-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch416:	0416-Allow-fractional-parts-in-disk-sizes.patch
Patch417:	0417-add-bash-completion-for-systemd-cgtop.patch
Patch418:	0418-execute-free-directory-path-if-we-fail-to-remove-it-.patch
Patch419:	0419-add-bash-completion-for-systemd-detect-virt.patch
Patch420:	0420-Do-not-print-invalid-UTF-8-in-error-messages.patch
Patch421:	0421-add-bash-completion-for-systemd-cat.patch
Patch422:	0422-journal-assume-that-next-entry-is-after-previous-ent.patch
Patch423:	0423-journal-forget-file-after-encountering-an-error.patch
Patch424:	0424-logind-ignore-failing-close-on-session-devices.patch
Patch425:	0425-core-introduce-new-stop-protocol-for-unit-scopes.patch
Patch426:	0426-core-watch-SIGCHLD-more-closely-to-track-processes-o.patch
Patch427:	0427-logind-rework-session-shutdown-logic.patch
Patch428:	0428-logind-order-all-scopes-after-both-systemd-logind.se.patch
Patch429:	0429-logind-given-that-we-can-now-relatively-safely-shutd.patch
Patch430:	0430-logind-fix-reference-to-systemd-user-sessions.servic.patch
Patch431:	0431-logind-add-forgotten-call-to-user_send_changed.patch
Patch432:	0432-logind-save-session-after-setting-the-stopping-flag.patch
Patch433:	0433-logind-save-user-state-after-stopping-the-session.patch
Patch434:	0434-logind-initialize-timer_fd.patch
Patch435:	0435-logind-pass-pointer-to-User-object-to-user_save.patch
Patch436:	0436-core-allow-PIDs-to-be-watched-by-two-units-at-the-sa.patch
Patch437:	0437-core-correctly-unregister-PIDs-from-PID-hashtables.patch
Patch438:	0438-logind-uninitialized-timer_fd-is-set-to-1.patch
Patch439:	0439-logind-add-forgotten-return-statement.patch
Patch440:	0440-core-fix-detection-of-dead-processes.patch
Patch441:	0441-Fix-prototype-of-get_process_state.patch
Patch442:	0442-core-check-for-return-value-from-get_process_state.patch
Patch443:	0443-man-update-link-to-LSB.patch
Patch444:	0444-man-systemd-bootchart-fix-spacing-in-command.patch
Patch445:	0445-man-add-missing-comma.patch
Patch446:	0446-build-sys-Don-t-distribute-generated-udev-rule.patch
Patch447:	0447-units-Do-not-unescape-instance-name-in-systemd-backl.patch
Patch448:	0448-util-add-timeout-to-generator-execution.patch
Patch449:	0449-input_id-Recognize-buttonless-joystick-types.patch
Patch450:	0450-logind-fix-policykit-checks.patch
Patch451:	0451-nspawn-don-t-try-mknod-of-dev-console-with-the-corre.patch
Patch452:	0452-build-sys-Find-the-tools-for-users-with-no-sbin-usr-.patch
Patch453:	0453-rules-mark-loop-device-as-SYSTEMD_READY-0-if-no-file.patch
Patch454:	0454-man-multiple-sleep-modes-are-to-be-separated-by-whit.patch
Patch455:	0455-man-fix-description-of-systemctl-after-before.patch
Patch456:	0456-udev-properly-detect-reference-to-unexisting-part-of.patch
Patch457:	0457-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch458:	0458-gpt-auto-generator-don-t-return-OOM-on-parentless-de.patch
Patch459:	0459-man-improve-wording-of-systemctl-s-after-before.patch
Patch460:	0460-cgroup-it-s-not-OK-to-invoke-alloca-in-loops.patch
Patch461:	0461-hwdb-update.patch
Patch462:	0462-core-don-t-try-to-relabel-mounts-before-we-loaded-th.patch
Patch463:	0463-man-explain-that-the-journal-field-SYSLOG_IDENTIFIER.patch
Patch464:	0464-man-be-more-specific-when-EnvironmentFile-is-read.patch
Patch465:	0465-systemctl-kill-mode-is-long-long-gone-don-t-mention-.patch
Patch466:	0466-systemctl-add-more-verbose-explanation-of-kill-who-a.patch
Patch467:	0467-ask-password-when-the-user-types-a-overly-long-passw.patch
Patch468:	0468-util-consider-both-fuse.glusterfs-and-glusterfs-netw.patch
Patch469:	0469-core-do-not-read-system-boot-timestamps-in-systemd-u.patch
Patch470:	0470-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch471:	0471-Add-hwdb-entry-for-Samsung-Series-7-Ultra.patch
Patch472:	0472-udev-do-not-export-static-node-tags-for-non-existing.patch
Patch473:	0473-journalctl-free-arg_file-on-exit.patch
Patch474:	0474-journal-fix-export-of-messages-containing-newlines.patch
Patch475:	0475-tty-ask-password-agent-return-negative-errno.patch
Patch476:	0476-systemd-python-use-.hex-instead-of-.get_hex.patch
Patch477:	0477-reduce-the-amount-of-messages-logged-to-dev-kmsg-whe.patch
Patch478:	0478-journal-cleanup-up-error-handling-in-update_catalog.patch
Patch479:	0479-hwdb-Update-database-of-Bluetooth-company-identifier.patch
Patch480:	0480-bash-completion-fix-__get_startable_units.patch
Patch481:	0481-hwdb-update.patch
Patch482:	0482-hwdb-PCI-include-primary-model-string-in-subsystem-m.patch
Patch483:	0483-sysctl-replaces-some-slashes-with-dots.patch
Patch484:	0484-man-document-relationship-between-RequiresMountsFor-.patch
Patch485:	0485-install-create_symlink-check-unlink-return-value.patch
Patch486:	0486-delta-do-not-use-unicode-chars-in-C-locale.patch
Patch487:	0487-core-print-debug-instead-of-error-message.patch




#Mageia patchset
Patch500:	0500-Clean-directories-that-were-cleaned-up-by-rc.sysinit.patch
Patch501:	0501-main-Add-failsafe-to-the-sysvinit-compat-cmdline-key.patch
Patch503:	0503-Disable-modprobe-pci-devices-on-coldplug-for-storage.patch
Patch504:	0504-Allow-booting-from-live-cd-in-virtualbox.patch
Patch505:	0505-reinstate-TIMEOUT-handling.patch
Patch506:	0506-udev-Allow-the-udevadm-settle-timeout-to-be-set-via-.patch
Patch507:	0507-Mageia-Relax-perms-on-sys-kernel-debug-for-lspcidrak.patch
Patch508:	0508-udev-rules-Apply-SuSE-patch-to-restore-cdrom-cdrw-dv.patch
Patch509:	0509-pam_systemd-Always-reset-XDG_RUNTIME_DIR.patch
Patch511:	0511-pam-Suppress-errors-in-the-SuSE-patch-to-unset-XDG_R.patch
Patch512:	0512-Revert-systemctl-skip-native-unit-file-handling-if-s.patch
Patch513:	0513-systemctl-Do-not-attempt-native-calls-for-enable-dis.patch

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
Requires(pre):	shadow-utils
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
BuildRequires:	distro-release-common >= 1:2012.0-0.4
# (tpg) just to be sure we install this libraries
Requires:	libsystemd-daemon = %{version}-%{release}
Requires:	libsystemd-login = %{version}-%{release}
Requires:	libsystemd-journal = %{version}-%{release}
Requires:	libsystemd-id128 = %{version}-%{release}
Requires:	nss_myhostname = %{version}-%{release}
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
%rename		systemd-tools

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

%package journal-gateway
Summary:		Gateway for serving journal events over the network using HTTP
Requires:		%{name} = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Obsoletes:		systemd < 206-7

%description journal-gateway
Offers journal events over the network using HTTP.

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
%rename		%{_lib}systemd-daemon0-devel

%description -n	%{libdaemon_devel}
Development files for the systemd-daemon shared library.

%package -n %{liblogin}
Summary:	Systemd-login library package
Group:		System/Libraries
Provides:	libsystemd-login = %{version}-%{release}

%description -n	%{liblogin}
This package provides the systemd-login shared library.

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
%rename		%{_lib}systemd-login0-devel

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
%rename		%{_lib}systemd-journal0-devel

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
%rename		%{_lib}systemd-id1280-devel

%description -n %{libid128_devel}
Development files for the systemd-id128 shared library.

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
#intltoolize --force --automake
autoreconf -fiv

%build
%global optflags %{optflags} -Os
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
%if %mdvver < 201300
	--with-distro=mandriva \
%endif
	--enable-chkconfig \
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
	--with-python \
	--with-kbd-loadkeys=/bin/loadkeys \
	--with-kbd-setfont=/bin/setfont

# FIXME workaround for uclibc-gcc finding glibc headers if uclibc doesn't
# have an equivalent header. This should be removed once uclibc-gcc does
# the right thing.
sed -i -e 's,#define HAVE_SYS_AUXV_H 1,#undef HAVE_SYS_AUXV_H,g' config.h
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
%if %mdvver < 201300
	--with-distro=mandriva \
%endif
	--enable-chkconfig \
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
rm -f %{buildroot}%{_sysconfdir}/systemd/system/display-manager.service

# Make sure these directories are properly owned
mkdir -p %{buildroot}/%{systemd_libdir}/system/basic.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/default.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/dbus.target.wants
mkdir -p %{buildroot}/%{systemd_libdir}/system/syslog.target.wants
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/getty.target.wants

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

mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/getty@.service.d
#install -m 0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/systemd/system/getty@.service.d/

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

# Make sure the NTP units dir exists
mkdir -p %{buildroot}%{systemd_libdir}/ntp-units.d/
install -m 0755 -d %{buildroot}%{_logdir}/journal

# (tpg) Install default distribution preset policy for services
mkdir -p %{buildroot}%{systemd_libdir}/system-preset/
mkdir -p %{buildroot}%{systemd_libdir}/user-preset/
# (tpg) install presets
install -m 0644 %{SOURCE12} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE13} %{buildroot}%{systemd_libdir}/system-preset/
install -m 0644 %{SOURCE14} %{buildroot}%{systemd_libdir}/system-preset/

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
/sbin/udevadm hwdb --update >/dev/null 2>&1 || :

#%post -n uclibc-udev
#%{uclibc_root}/bin/systemctl --quiet try-restart systemd-udevd.service >/dev/null 2>&1 || :

%pre
# (cg) Cannot use rpm-helper scripts as it results in a cyclical dep as
# rpm-helper requires systemd-units which in turn requires systemd...
if ! getent group %{name}-journal >/dev/null 2>&1; then
	/usr/sbin/groupadd -r %{name}-journal >/dev/null || :
fi

if [ $1 -ge 2 ]; then
systemctl stop stop systemd-udevd-control.socket systemd-udevd-kernel.socket systemd-udevd.service >/dev/null 2>&1 || :
fi

%post
/usr/bin/systemd-machine-id-setup >/dev/null 2>&1 || :
/usr/lib/systemd/systemd-random-seed save >/dev/null 2>&1 || :
/usr/bin/systemctl daemon-reexec >/dev/null 2>&1 || :
/usr/bin/systemctl start systemd-udevd.service >/dev/null 2>&1 || :
/usr/bin/systemctl restart systemd-localed.service >/dev/null 2>&1 || :
/usr/bin/journalctl --update-catalog >/dev/null 2>&1 || :

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

# (tpg) move sysctl.conf to /etc/sysctl.d as since 207 /etc/sysctl.conf is skipped
if [ $1 -ge 2 ]; then
    if [ -e %{_sysconfdir}/sysctl.conf ] && [ ! -L %{_sysconfdir}/sysctl.conf ]; then
	mv -f %{_sysconfdir}/sysctl.conf %{_sysconfdir}/sysctl.d/99-sysctl.conf
	ln -s %{_sysconfdir}/sysctl.d/99-sysctl.conf %{_sysconfdir}/sysctl.conf
    fi
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

%triggerun -- %{name} < 208-2
chgrp -R systemd-journal /var/log/journal || :
chmod 02755 /var/log/journal || :
if [ -f /etc/machine-id ]; then
	chmod 02755 /var/log/journal/$(cat /etc/machine-id) || :
fi

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


%pre journal-gateway
%_pre_groupadd systemd-journal systemd-journal-gateway
%_pre_useradd systemd-journal-gateway %{_var}/run/%{name}-journal-gateway /bin/false
%_pre_groupadd systemd-journal-gateway systemd-journal-gateway

%post journal-gateway
%_post_service systemd-journal-gatewayd.socket
%_post_service systemd-journal-gatewayd.service

%preun journal-gateway
%_preun_service systemd-journal-gatewayd.socket
%_preun_service systemd-journal-gatewayd.service

%postun journal-gateway
%_postun_service systemd-journal-gatewayd.service

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
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user
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
%dir %{python_sitearch}/%{name}
%attr(02755,root,systemd-journal) %dir %{_logdir}/journal
%{_sysconfdir}/xdg/systemd
%{_initrddir}/README
%{_logdir}/README

# (tpg) from sysvinit subpackage
/sbin/init
/bin/reboot
/bin/halt
/bin/poweroff
/sbin/shutdown
/sbin/telinit
/sbin/runlevel
#
/bin/systemd-ask-password
/bin/systemd-notify
/bin/systemd-tmpfiles
/bin/systemd-tty-ask-password-agent
/bin/systemd
/bin/journalctl
/bin/loginctl
/bin/systemd-inhibit
/sbin/systemd-machine-id-setup
%{_bindir}/systemd-analyze
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
%{systemd_libdir}/systemd-backlight
%{systemd_libdir}/systemd-binfmt
%{systemd_libdir}/systemd-c*
%{systemd_libdir}/systemd-fsck
%{systemd_libdir}/systemd-hostnamed
%{systemd_libdir}/systemd-initctl
%{systemd_libdir}/systemd-journald
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
%{systemd_libdir}/system-preset/*.preset
/usr/lib/tmpfiles.d/*.conf
/%{_lib}/security/pam_systemd.so
%{_var}/lib/rpm/filetriggers/systemd-daemon-reload.*
%{_bindir}/systemd-cgls
%{_bindir}/systemd-nspawn
%{_bindir}/systemd-stdio-bridge
%{_bindir}/systemd-cat
%{_bindir}/systemd-cgtop
%{_mandir}/man1/bootctl.1.*
%{_mandir}/man1/busctl.1.*
%{_mandir}/man1/init.*
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
%{_mandir}/man8/halt.*
%{_mandir}/man8/reboot.*
%{_mandir}/man8/shutdown.*
%{_mandir}/man8/poweroff.*
%{_mandir}/man8/telinit.*
%{_mandir}/man8/runlevel.*
%{_mandir}/man8/pam_systemd.*
%{_mandir}/man8/systemd-activate.8.*
%{_mandir}/man8/systemd-ask-*.8.*
%{_mandir}/man1/systemd-analyze.1*
%{_mandir}/man8/systemd-backlight*.8.*
%{_mandir}/man8/systemd-binfmt*.8.*
%{_mandir}/man8/systemd-cryptsetup*.8.*
%{_mandir}/man8/systemd-efi-boot-generator*.8.*
%{_mandir}/man8/systemd-gpt-auto-generator*.8.*
%{_mandir}/man8/systemd-fsck*.8.*
%{_mandir}/man8/systemd-fstab*.8.*
%{_mandir}/man8/systemd-getty*.8.*
%{_mandir}/man8/systemd-halt*.8.*
%{_mandir}/man8/systemd-hibernate*.8.*
%{_mandir}/man8/systemd-hostnamed*.8.*
%{_mandir}/man8/systemd-hybrid*.8.*
%{_mandir}/man8/systemd-initctl*.8.*
%{_mandir}/man8/systemd-journald.8.*
%{_mandir}/man8/systemd-journald.service.8.*
%{_mandir}/man8/systemd-journald.socket.8.*
%{_mandir}/man8/systemd-kexec*.8.*
%{_mandir}/man8/systemd-localed*.8.*
%{_mandir}/man8/systemd-logind*.8.*
%{_mandir}/man8/systemd-machined*.8.*
%{_mandir}/man8/systemd-modules*.8.*
%{_mandir}/man8/systemd-poweroff*.8.*
%{_mandir}/man8/systemd-quota*.8.*
%{_mandir}/man8/systemd-random*.8.*
%{_mandir}/man8/systemd-readahead*.8.*
%{_mandir}/man8/systemd-reboot*.8.*
%{_mandir}/man8/systemd-remount*.8.*
%{_mandir}/man8/systemd-shutdown*.8.*
%{_mandir}/man8/systemd-sleep*.8.*
%{_mandir}/man8/systemd-suspend*.8.*
%{_mandir}/man8/systemd-sysctl*.8.*
%{_mandir}/man8/systemd-system*.8.*
%{_mandir}/man8/systemd-timedated*.8.*
%{_mandir}/man8/systemd-tmpfiles*.8.*
%{_mandir}/man8/systemd-udev*.8.*
%{_mandir}/man8/systemd-update*.8.*
%{_mandir}/man8/systemd-user*.8.*
%{_mandir}/man8/systemd-vconsole*.8.*
%{_mandir}/man8/kernel-install.*

# tools
%{python_sitearch}/%{name}/*.py*
%{python_sitearch}/%{name}/*.so

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

%files units
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/system/getty.target.wants
%dir %{_sysconfdir}/systemd/system/getty@.service.d
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%dir %{systemd_libdir}/system
%dir %{systemd_libdir}/system/basic.target.wants
%dir %{systemd_libdir}/system/bluetooth.target.wants
%dir %{systemd_libdir}/system/dbus.target.wants
%dir %{systemd_libdir}/system/default.target.wants
%dir %{systemd_libdir}/system/local-fs.target.wants
%dir %{systemd_libdir}/system/multi-user.target.wants
%dir %{systemd_libdir}/system/runlevel1.target.wants
%dir %{systemd_libdir}/system/runlevel2.target.wants
%dir %{systemd_libdir}/system/runlevel3.target.wants
%dir %{systemd_libdir}/system/runlevel4.target.wants
%dir %{systemd_libdir}/system/runlevel5.target.wants
%dir %{systemd_libdir}/system/sockets.target.wants
%dir %{systemd_libdir}/system/sysinit.target.wants
%dir %{systemd_libdir}/system/syslog.target.wants
%dir %{systemd_libdir}/system/timers.target.wants
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/catalog
%dir %{_prefix}/lib/systemd/ntp-units.d
%dir %{_prefix}/lib/systemd/system-generators
%dir %{_prefix}/lib/systemd/user
%dir %{_prefix}/lib/systemd/user-generators
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/*
%{_datadir}/zsh/site-functions/*
/bin/systemctl
/bin/machinectl
%{_bindir}/systemctl
%{_sysconfdir}/profile.d/40systemd.sh
%{_sysconfdir}/rpm/macros.d/systemd.macros
%{systemd_libdir}/system/local-fs.target.wants/*.service
%{systemd_libdir}/system/local-fs.target.wants/*.mount
%{systemd_libdir}/system/multi-user.target.wants/*.target
%{systemd_libdir}/system/multi-user.target.wants/*.path
%{systemd_libdir}/system/multi-user.target.wants/*.service
%{systemd_libdir}/system/runlevel*.target.wants/*.service
%{systemd_libdir}/system/sockets.target.wants/*.socket
%{systemd_libdir}/system/sysinit.target.wants/*.target
%{systemd_libdir}/system/sysinit.target.wants/*.*mount
%{systemd_libdir}/system/sysinit.target.wants/*.service
%{systemd_libdir}/system/sysinit.target.wants/*.path
%{systemd_libdir}/system/timers.target.wants/*.timer
%{systemd_libdir}/system/*.automount
%{systemd_libdir}/system/*.mount
%{systemd_libdir}/system/*.path
%{systemd_libdir}/system/auto*.service
%{systemd_libdir}/system/console*.service
%{systemd_libdir}/system/dbus-org*.service
%{systemd_libdir}/system/de*.service
%{systemd_libdir}/system/emergency*.service
%{systemd_libdir}/system/getty*.service
%{systemd_libdir}/system/halt-*.service
%{systemd_libdir}/system/initrd-*.service
%{systemd_libdir}/system/kmod-*.service
%{systemd_libdir}/system/quota*.service
%{systemd_libdir}/system/rc-*.service
%{systemd_libdir}/system/rescue*.service
%{systemd_libdir}/system/serial-*.service
%{systemd_libdir}/system/systemd-ask-password*.service
%{systemd_libdir}/system/systemd-backlight*.service
%{systemd_libdir}/system/systemd-binfmt*.service
%{systemd_libdir}/system/systemd-fsck*.service
%{systemd_libdir}/system/systemd-halt*.service
%{systemd_libdir}/system/systemd-hibernate*.service
%{systemd_libdir}/system/systemd-hostnamed*.service
%{systemd_libdir}/system/systemd-hybrid*.service
%{systemd_libdir}/system/systemd-initctl*.service
%{systemd_libdir}/system/systemd-journal-flush.service
%{systemd_libdir}/system/systemd-journald.service
%{systemd_libdir}/system/systemd-kexec*.service
%{systemd_libdir}/system/systemd-localed*.service
%{systemd_libdir}/system/systemd-logind*.service
%{systemd_libdir}/system/systemd-machined.service
%{systemd_libdir}/system/systemd-modules-load.service
%{systemd_libdir}/system/systemd-nspawn*.service
%{systemd_libdir}/system/systemd-poweroff.service
%{systemd_libdir}/system/systemd-quotacheck.service
%{systemd_libdir}/system/systemd-random*service
%{systemd_libdir}/system/systemd-readahead*.service
%{systemd_libdir}/system/systemd-readahead*.timer
%{systemd_libdir}/system/systemd-reboot.service
%{systemd_libdir}/system/systemd-remount*.service
%{systemd_libdir}/system/systemd-shutdownd.service
%{systemd_libdir}/system/systemd-suspend.service
%{systemd_libdir}/system/systemd-sysctl.service
%{systemd_libdir}/system/systemd-timedated.service
%{systemd_libdir}/system/systemd-tmpfiles-*.service
%{systemd_libdir}/system/systemd-tmpfiles-*.timer
%{systemd_libdir}/system/systemd-udev*.service
%{systemd_libdir}/system/systemd-update-*.service
%{systemd_libdir}/system/systemd-user-*.service
%{systemd_libdir}/system/systemd-vconsole-*.service
%{systemd_libdir}/system/udev*.service
%{systemd_libdir}/system/user*.service

%{systemd_libdir}/system/*.slice

%{systemd_libdir}/system/syslog.socket
%{systemd_libdir}/system/systemd-initctl.socket
%{systemd_libdir}/system/systemd-journald.socket
%{systemd_libdir}/system/systemd-shutdownd.socket
%{systemd_libdir}/system/systemd-udev*.socket
%{systemd_libdir}/system/*.target

%{_prefix}/lib/systemd/catalog/*.catalog
%{_prefix}/lib/systemd/user/*.service
%{_prefix}/lib/systemd/user/*.target
%{_mandir}/man1/systemctl.*

%files journal-gateway
%dir %{_datadir}/systemd/gatewayd
%{systemd_libdir}/systemd-journal-gatewayd
%{systemd_libdir}/system/systemd-journal-gatewayd.service
%{systemd_libdir}/system/systemd-journal-gatewayd.socket
%{_mandir}/man8/systemd-journal-gatewayd.*
%{_datadir}/systemd/gatewayd/browse.html

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
