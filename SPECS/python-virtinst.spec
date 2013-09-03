# -*- rpm-spec -*-

%define _version 0.600.0
%define _release 16

%define with_rhel6_defaults 1
%define with_selinux 1

%define with_sbin_compat 1

# End local config

%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# This macro is used for the continuous automated builds. It just
# allows an extra fragment based on the timestamp to be appended
# to the release. This distinguishes automated builds, from formal
# Fedora RPM builds
%define _extra_release %{?dist:%{dist}}%{!?dist:%{?extra_release:%{extra_release}}}

%define appname virtinst

%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%define with_egg 1
%else
%define with_egg 0
%endif


Summary: Python modules and utilities for installing virtual machines
Name: python-%{appname}
Version: %{_version}
Release: %{_release}%{_extra_release}
Source0: http://virt-manager.org/download/sources/%{appname}/%{appname}-%{version}.tar.gz
# Fix installation of translation files
Patch1: %{appname}-fix-po-install.patch
# Regenerate man pages to actually fix doc bugs (bz 694713)
Patch2: %{appname}-regenerate-man-pages.patch
# virt-install: Fix --initrd-inject (bz 729643)
Patch3: %{appname}-fix-initrd-inject.patch
# virt-install: Fix --file-size and --prompt (bz 729608)
Patch4: %{appname}-fix-filesize-prompt.patch
# Fix changing disk bus in virt-manager (bz 728423)
Patch5: %{appname}-fix-vmm-disk-bus.patch
# virt-install: Fix --cpu with case sensitive CPU model (bz 727986)
Patch6: %{appname}-lowercase-cpu-model.patch
# Fix remote URL installs as root (bz 546440)
Patch7: %{appname}-fix-remote-url.patch
# Add QED volume support (bz 739487)
Patch8: %{appname}-qed-vol.patch
# virt-install: Fix --nonetworks (bz 738216)
Patch9: %{appname}-fix-nonetworks.patch
# virt-install: Fix --location with qemu:///session (bz 738211)
Patch10: %{appname}-fix-usermode-url.patch
# Don't leave host PCI devices in unusable state on hotplug fail (bz 746355)
Patch11: %{appname}-hostdev-detach.patch
# Configure clock to avoid timer drift for windows (bz 742736)
Patch12: %{appname}-windows-clock-catchup.patch
# Fix random virt-manager traceback when creating guests (bz 765928)
Patch13: %{appname}-xml-dict-locking.patch
# Fix specifying over 26 virtio disks (bz 769191)
Patch14: %{appname}-virtio-27-targets.patch
# Fix a japanese translation issue (bz 783866)
Patch15: %{appname}-translation-fix.patch
# Fix virt-manager guest listing when <description> is empty (bz 786672)
Patch16: %{appname}-fix-vmm-guest-listing.patch
# Use correct MAC prefix when cloning KVM guests (bz 798909)
Patch17: %{appname}-fix-clone-mac.patch
# Escape string when setting VM description (bz 741158)
Patch18: %{appname}-escape-desc-string.patch
Patch19: %{appname}-add-address-element-in-hostdev-xml-when-the-values-a.patch
Patch20: %{appname}-Don-t-copy-USB-bus-address-by-default-from-node-devi.patch
Patch21: %{appname}-Add-cpuset-auto-test-confirming-it-actually-works.patch
Patch22: %{appname}-Allow-specifying-security-.relabel-yes.patch
Patch23: %{appname}-Add-RHEL7-to-osdict.patch
Patch24: %{appname}-Fix-cpuset-auto.patch
Patch25: %{appname}-Support-multiple-seclabels.patch
Patch26: %{appname}-setup-rebuild-manpages-in-build-phase.patch
Patch27: %{appname}-Remove-and-ignore-build-generated-files.patch
Patch28: %{appname}-build-One-more-fix-for-clean-builds.patch
Patch29: %{appname}-Update-pod-file-from-latest-pod.in.patch

#centos xen-c6 patches
Patch1000: virtinst-xen4-tap2.patch

License: GPLv2+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Url: http://virt-manager.org
Provides: virt-install
Provides: virt-clone
Provides: virt-image
Provides: virt-convert
Requires: libvirt-python >= 0.2.0
Requires: urlgrabber
Requires: libxml2-python
Requires: python-urlgrabber
%if %{with_selinux}
Requires: libselinux-python
%endif
BuildRequires: gettext
BuildRequires: python
BuildRequires: /usr/bin/pod2man

%description
virtinst is a module that helps build and install libvirt based virtual
machines. Currently supports KVM, QEmu and Xen virtual machines. Package
includes several command line utilities, including virt-install (build
and install new VMs) and virt-clone (clone an existing virtual machine).

%prep
%setup -q -n %{appname}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1

#centos xen-c6 patches
%patch1000 -p1

%build
%if %{with_rhel6_defaults}
%define _rhel6_defaults --rhel6defaults
%endif

python setup.py build \
    %{?_rhel6_defaults}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT --skip-build

%if %{with_sbin_compat}
# Back compat in case people hardcoded old /usr/sbin/virt-install location
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
ln -s ../bin/virt-install $RPM_BUILD_ROOT/%{_sbindir}/virt-install
%endif

%find_lang %{appname} || echo 0

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{appname}.lang
%defattr(-,root,root)
%doc README COPYING AUTHORS ChangeLog NEWS doc/image.rng doc/example1.xml
%dir %{python_sitelib}/%{appname}
%dir %{python_sitelib}/virtconv
%{python_sitelib}/%{appname}/*
%{python_sitelib}/virtconv/*
%if %{with_egg}
%{python_sitelib}/%{appname}-*.egg-info
%endif
%{_mandir}/man1/*
%{_mandir}/man5/*
%if %{with_sbin_compat}
%{_sbindir}/virt-install
%endif
%{_bindir}/virt-install
%{_bindir}/virt-clone
%{_bindir}/virt-image
%{_bindir}/virt-convert

%changelog
* Fri Jun 14 2013 Johnny Hughes <johnny@centos.org> - 0.600.0-16
- roll in tap2 support for xen 

* Tue Jan 08 2013 Jiri Denemark <jdenemar@redhat.com> - 0.600.0-15
- build: One more fix for clean builds (rhbz#832339)
- Update pod file from latest pod.in (rhbz#832339)

* Wed Dec 12 2012 Jiri Denemark <jdenemar@redhat.com> - 0.600.0-14
- setup: rebuild manpages in build phase (rhbz#832339)
- Remove and ignore build-generated files (rhbz#832339)

* Wed Dec 05 2012 Jiri Denemark <jdenemar@redhat.com> - 0.600.0-13
- Support multiple seclabels (rhbz#832339)

* Wed Oct 31 2012 Jiri Denemark <jdenemar@redhat.com> - 0.600.0-12
- Fix cpuset=auto (rhbz#834495)

* Fri Oct 19 2012 Cole Robinson <crobinso@redhat.com> - 0.600.0-11
- More fixes for USB product/vendor + bus/addr (bz #820303)

* Fri Oct 19 2012 Cole Robinson <crobinso@redhat.com> - 0.600.0-10
- Fix relabel support (bz #832339)

* Fri Oct 12 2012 Jiri Denemark <jdenemar@redhat.com> - 0.600.0-9
- Add RHEL7 to osdict (rhbz#803631)
- Allow specifying --security ...relabel=yes|no (rhbz#832339)
- Fix some issues with relabel= support (rhbz#832339)
- Add --cpuset=auto test confirming it actually works (rhbz#834495)
- Don't copy USB bus/address by default from node device (rhbz#820303)
- Add address element in hostdev xml when the values are present (rhbz#820303)

* Mon Apr 02 2012 Cole Robinson <crobinso@redhat.com> - 0.600.0-8
- Use correct MAC prefix when cloning KVM guests (bz 798909)
- Escape string when setting VM description (bz 741158)

* Thu Feb 09 2012 Cole Robinson <crobinso@redhat.com> - 0.600.0-7
- Fix virt-manager guest listing when <description> is empty (bz 786672)

* Wed Feb 01 2012 Cole Robinson <crobinso@redhat.com> - 0.600.0-6
- Fix random virt-manager traceback when creating guests (bz 765928)
- Fix specifying over 26 virtio disks (bz 769191)
- Fix a japanese translation issue (bz 783866)

* Tue Oct 18 2011 Cole Robinson <crobinso@redhat.com> - 0.600.0-5
- Don't leave host PCI devices in unusable state on hotplug fail (bz
  746355)
- Configure clock to avoid timer drift for windows (bz 742736)

* Thu Oct 13 2011 Cole Robinson <crobinso@redhat.com> - 0.600.0-4
- Add QED volume support (bz 739487)
- virt-install: Fix --nonetworks (bz 738216)
- virt-install: Fix --location with qemu:///session (bz 738211)

* Tue Aug 30 2011 Cole Robinson <crobinso@redhat.com> - 0.600.0-3
- virt-install: Fix --initrd-inject (bz 729643)
- virt-install: Fix --file-size and --prompt (bz 729608)
- Fix changing disk bus in virt-manager (bz 728423)
- virt-install: Fix --cpu with case sensitive CPU model (bz 727986)
- Fix remote URL installs as root (bz 546440)

* Tue Aug 02 2011 Cole Robinson <crobinso@redhat.com> - 0.600.0-2
- Fix installation of translation files
- Regenerate man pages to actually fix doc bugs (bz 694713)

* Tue Jul 26 2011 Cole Robinson <crobinso@redhat.com> - 0.600.0-1.el6
- Rebased to version 0.600.0
- virt-install: Various improvements to enable LXC/container guests:
- New --filesystem option for <filesystem> devices
- New --init option for container <init> path
- New --container option (similar to --paravirt or --hvm)
- virt-install: Make --location  remotely (with latest libvirt)
- virt-install: New --smartcard option for <smartcard> devices
- (Marc-André Lureau)
- virt-install: New --numatune option for building guest <numatune> XML
- virt-install: option to set --disk error_policy=
- virt-install: option to set --disk serial=

* Wed Mar 30 2011 Cole Robinson <crobinso@redhat.com> - 0.500.5-3.el6
- virt-install: Actually fix --check-cpu error message (bz 676995)
- virt-install: Actually fix --print-step typos (bz 683320)
- virt-install: Regenerate man pages for async IO options (bz 611205)

* Wed Mar 09 2011 Cole Robinson <crobinso@redhat.com> - 0.500.5-2.el6
- Fix --check-cpu error message (bz 676995)
- Fix bogus virt-convert output (bz 678214)
- virt-install: Fix --print-step typos (bz 683320)
- Fix parsing domain <features> (bz 683100)
- virt-convert: Preserve storage format in generated XML (bz 622684)
- Fix specifying manual spice port (bz 682697)
- Fix nonsparse disk creation (bz 678374)
- Properly raise errors when creating storage (bz 683182)
- Fix using a pool source as storage (bz 589665)
- Support sound model 'ich6' (bz 683103)
- Use async IO properly for storage (bz 611205)

* Fri Jan 14 2011 Cole Robinson <crobinso@redhat.com> - 0.500.5-1.el6
- Rebase to 0.500.5 (bz 658963)
- New virt-install --cpu option for configuring CPU model/features
- virt-install --vcpus option can not specify topology and maxvcpus
- New virt-install --graphics option to unify --vnc, --sdl, spice config
- New virt-install --print-xml option to skip install and print XML

* Mon Aug 02 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-7.el6
- Fix using qcow2 disk images via virt-install (bug 620456)

* Wed Jul 21 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-6.el6
- Fix CDROM installs backed by physical CDROM device (bug 616480)

* Mon Jun 28 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-5.el6
- Fix windows installs, actually attach CDROM for second stage (bz 607083)

* Mon Jun 21 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-4.el6
- Fix pool enumeration in virt-manager (bz 603864)

* Tue May 25 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-3.el6
- Default to disk cache=none (bz 574983)

* Thu May 13 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-2.el6
- Fix --cdrom with media manually added to pool (bz 574973)
- Handle commas in security labels (bz 581473)
- virt-install: Fix --location dvd.iso (bz 587679)

* Wed Mar 24 2010 Cole Robinson <crobinso@redhat.com> - 0.500.3-1.el6
- Rebase to 0.500.3
- virt-install: New --watchdog option: configure a virtual watchdog device
- virt-install: New --soundhw option: More flexible sound configuration
                deprecates --sound, though back compat is maintained
- virt-install: New --security option: configure VM security driver settings
- virt-install: New --description option: set a human readable description
- Better OS defaults: Use <video> VGA and <sound> AC97 if supported

* Thu Jan 14 2010 Cole Robinson <crobinso@redhat.com> - 0.500.1-3.el6
- Fix building with egginfo files

* Wed Dec 09 2009 Cole Robinson <crobinso@redhat.com> - 0.500.1-2.fc12
- Fix interface API detection for libvirt < 0.7.4

* Thu Dec  3 2009 Cole Robinson <crobinso@redhat.com> - 0.500.1-1.fc12
- Update to version 0.500.1
- virt-install now attempts --os-variant detection by default.
- New --disk option 'format', for creating image formats like qcow2 or vmdk
- Many improvements and bugfixes

* Mon Oct 05 2009 Cole Robinson <crobinso@redhat.com> - 0.500.0-5.fc12
- Update translations (bz 493795)

* Thu Sep 24 2009 Cole Robinson <crobinso@redhat.com> - 0.500.0-4.fc12
- Don't use usermode net for non-root qemu:///system via virt-install
- Fix cdrom installs where the iso is a storage volume (bz 524109)
- Fix path permissions for kernel/initrd download location (bz 523960)

* Wed Sep 16 2009 Cole Robinson <crobinso@redhat.com> - 0.500.0-3.fc12
- Don't generate bogus disk driver XML.
- Add '--disk format=' for specifying format (qcow2, ...) when provisioning
- Add Fedora12 to os dictionary

* Sun Sep 13 2009 Cole Robinson <crobinso@redhat.com> - 0.500.0-2.fc12
- Don't erroneously set limit for amount of virtio devices (bz 499654)
- Don't use virtio for cdrom devices (bz 517151)
- Auto detect keymapping (bz 487735)

* Tue Jul 28 2009 Cole Robinson <crobinso@redhat.com> - 0.500.0-1.fc12
- Update to version 0.500.0
- New virt-install device options --serial, --parallel, and --video
- Allow various auth types for libvirt connections (PolicyKit, SASL, ...)
- New virt-clone option --auto-clone: generates all needed input.
- Specify network device model via virt-install --network (Guido Gunther)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.400.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Cole Robinson <crobinso@redhat.com> - 0.400.3-8.fc12
- Fix PCI assignment (bz 499267)

* Tue Apr 21 2009 Cole Robinson <crobinso@redhat.com> - 0.400.3-7.fc11
- Only warn if selinux labeling appears to be wrong (bz 496340)

* Tue Apr 14 2009 Cole Robinson <crobinso@redhat.com> - 0.400.3-6.fc11
- More translation updates

* Thu Apr 9 2009 Cole Robinson <crobinso@redhat.com> - 0.400.3-5.fc11
- Don't set a keymap if user doesn't specify one (bz 487737)
- Fix adding floppy devices (bz 493408)
- Updated translations (bz 493944, bz 494358)

* Fri Apr  3 2009 Daniel P. Berrange <berrange@redhat.com> - 0.400.3-4.fc11
- Attempt to fix SELinux labelling on CDROM ISOs used for installation

* Fri Apr  3 2009 Daniel P. Berrange <berrange@redhat.com> - 0.400.3-3.fc11
- Set SELinux context on $HOME/.virtinst to make kernel/initrd boot work (rhbz #491052)

* Mon Mar 23 2009 Cole Robinson <crobinso@redhat.com> - 0.400.3-2.fc11
- Add spanish translation (bz 480816)
- Fix calls to libvirt host device detach/reset
- Fix virt-image with create-on-the-fly disks

* Tue Mar 10 2009 Cole Robinson <crobinso@redhat.com> - 0.400.3-1.fc11
- Update to bugfix release 0.400.3
- Fix virt-install --os-type windows installs
- Fix URL installs to not wipe out --os-variant value

* Thu Mar  5 2009 Cole Robinson <crobinso@redhat.com> - 0.400.2-3.fc11
- Fix virt-install --file option (bz 488731)

* Wed Mar  4 2009 Cole Robinson <crobinso@redhat.com> - 0.400.2-2.fc11
- Update polish translation (bz 310781)

* Tue Mar  3 2009 Cole Robinson <crobinso@redhat.com> - 0.400.2-1.fc11
- Update to version 0.400.2
- virt-install --import option for creating a guest from an existing disk
- virt-install --host-device option for host device passthrough
- virt-clone --original-xml for cloning from an xml file
- virt-install --nonetworks option.

* Fri Feb 27 2009 Daniel P. Berrange <berrange@redhat.com> - 0.400.1-3.fc11
- Add Fedora 11 OS type with USB tablet (rhbz #487028)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.400.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Cole Robinson <crobinso@redhat.com> - 0.400.1-1.fc11
- Update to 0.400.1
- virt-convert virt-image -> vmx support
- virt-image checksum support
- Improved URL fetching support (Debian Xen, Ubuntu kernel + boot.iso)

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.400.0-7
- Rebuild for Python 2.6

* Tue Dec  2 2008 Cole Robinson <crobinso@redhat.com> - 0.400.0-6.fc11
- Fix printing translated help messages
- Allow using virtio to pxe boot

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.400.0-5
- Rebuild for Python 2.6

* Mon Oct 27 2008 Cole Robinson <crobinso@redhat.com> - 0.400.0-4.fc10
- Updated translations (bz 467810)
- Specific os entry for XP 64 (bz 467851)
- Disk pool 'dos' format fix

* Mon Oct 20 2008 Cole Robinson <crobinso@redhat.com> - 0.400.0-3.fc10
- Fix missing variable error (bz 467228)

* Tue Oct 14 2008 Cole Robinson <crobinso@redhat.com> - 0.400.0-2.fc10
- Updated polish translation (bz 310781)
- Fix error accessing os dictionary in virt-convert
- Log tracebacks from cli apps
- Better default connection detection for qemu/kvm
- Set up virtio for f9 guests (bz 462404)
- Don't report option collision if using --bridge
- Update storage pool when looking up volume (bz 465551)

* Wed Sep 10 2008 Cole Robinson <crobinso@redhat.com> - 0.400.0-1.fc10
- Add virt-convert tool
- Add virt-pack tool
- virt-install --disk option for using/provisioning libvirt storage
- virt-install remote installation support
- virt-install --sound option to add soundcard emulation

* Wed Jun  4 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.3-7.fc10
- Fix fetching of HVM kernels (rhbz #450032)

* Fri May  9 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.3-6.fc10
- Use /var/lib/libvirt/boot for kernel/initrd images (rhbz #445854)

* Tue Apr  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.3-5.fc9
- Added Serbian translation

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.3-4.fc9
- Added italian translation

* Tue Apr 1 2008 Cole Robinson <crobinso@redhat.com> - 0.300.3-3.fc9
- Revert unintentionally committed spec change.

* Thu Mar 27 2008 Cole Robinson <crobinso@redhat.com> - 0.300.3-2.fc9
- Keep qemu cdrom device after first stage of install. (rhbz #244802)
- Fix default guest arch regression from virt-install
- Pass extra args to a fullvirt guest from virt-install
- Update polish translation

* Mon Mar 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.3-1.fc9
- Update to 0.300.3 release

* Thu Jan 31 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.2-3.fc9
- Disable virt-viewer dep to allow non-X installs (rhbz #387971)

* Thu Jan 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.2-2.fc9
- Added dep on libxml2-python and python-urlgrabber

* Thu Jan 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.300.2-1.fc9
- Update to 0.300.2 release

* Thu Oct 11 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.1-3.fc8
- Fix missing file exception check with NFS installs (rhbz #325591)

* Thu Oct  4 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.1-2.fc8
- Remove USB tablet for all except Windows (rhbz #302951)

* Tue Sep 25 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.1-1.fc8
- Update to 0.300.1 release
- Added PXE support

* Wed Sep 19 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.0-4.fc8
- Fix post install CDROM config for KVM guests

* Tue Sep 11 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.0-3.fc8
- Fixed default architecture. Again.

* Tue Sep 11 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.0-2.fc8
- Fixed detection of Fedora 8 distro trees (rhbz #273781)

* Wed Aug 29 2007 Daniel P. Berrange <berrange@redhat.com> - 0.300.0-1.fc8
- Updated to 0.300.0
- Added virt-image tool
- Switched to calling virsh console and virt-viewer
- Improved user input validation

* Fri Aug 24 2007 Daniel P. Berrange <berrange@redhat.com> - 0.200.0-3.fc8
- Remove ExludeArch since libvirt is now available everywhere

* Thu Jul 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.200.0-2.fc8
- Fixed default architecture

* Tue Jul 18 2007 Daniel P. Berrange <berrange@redhat.com> - 0.200.0-1.fc8
- Updated to 0.200.0
- Added virt-clone tool
- Added manual pages

* Tue May  1 2007 Daniel P. Berrange <berrange@redhat.com> - 0.103.0-3.fc7
- Fixed module import when using --accelerate
- Fixed detection of RHEL5 client distro
- Fixed default 'network's selection & default URI choice to
  not be Xen specific
- Fixed features XML when using initrd for fullvirt

* Tue Apr 17 2007 Mark McLoughlin <markmc@redhat.com> - 0.103.0-2.fc7
- Fix urlgrabber import error

* Mon Apr 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.103.0-1.fc7
- Updated to 0.103.0 release
- More validation of UUIDs
- Automatically reboot Windows guests with CDROM still attached
- Allow '-'  in guest names
- Adjust way distro detection is done

* Tue Mar 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.102.0-1.fc7
- Updated to 0.102.0 release

* Thu Mar  8 2007 Daniel P. Berrange <berrange@redhat.com> - 0.101.0-4.fc7
- Fixed install of paravirt Xen guests

* Fri Mar  2 2007 Daniel P. Berrange <berrange@redhat.com> - 0.101.0-3.fc7
- Fixed restart of guests after install completes

* Tue Feb 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.101.0-2.fc7
- Remove obsolete patches

* Tue Feb 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.101.0-1.fc7
- Updated to 0.101.0 to enable QEMU support

* Thu Jan 25 2007 Daniel P. Berrange <berrange@redhat.com> - 0.100.0-3.fc7
- Make back-compat with old APIs for Cobbler sanity

* Thu Jan 25 2007 Daniel P. Berrange <berrange@redhat.com> - 0.100.0-2.fc7
- Fix errors with NFS mount based installs

* Mon Jan 22 2007 Daniel P. Berrange <berrange@redhat.com> - 0.100.0-1.fc7
- Updated to 0.100.0 which now uses libvirt inactive domain support
  needed to operate correctly against xen 3.0.4

* Tue Dec 18 2006 Daniel P. Berrange <berrange@redhat.com> - 0.98.0-3.fc7
- don't traceback on invalid memory param (gcosta, #219270)
- let the console come back quicker to help with HVM installs (#212024)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.98.0-2
- rebuild for python 2.5

* Thu Nov 30 2006 Jeremy Katz <katzj@redhat.com> - 0.98.0-1
- add support for creating nonsparse disk images (#217764)
- remove xeninst compat bits

* Mon Nov 20 2006 Jeremy Katz <katzj@redhat.com> - 0.97.0-1
- handle multiple nics/disks on virt-install command line (#215726)
- buildrequire python

* Wed Oct 18 2006 Jeremy Katz <katzj@redhat.com> - 0.96.0-1
- improve check for if a machine is hvm capable to catch when support isn't
  allowed by the bios (#211276)
- cleanup after nfs mount failure on pv install (#206196)
- support for setting vcpus (#210516)

* Thu Oct 12 2006 Jeremy Katz <katzj@redhat.com> - 0.95.0-1
- support for blktap (danpb)
- name change

* Tue Oct  3 2006 Jeremy Katz <katzj@redhat.com> - 0.94.0-1
- Fix using block device as backing (#209138)
- Fix error handling for invalid install locations (danpb)
- Write out vcpu config (danpb)

* Wed Sep 20 2006 Jeremy Katz <katzj@redhat.com> - 0.93.0-1
- Fix hvm network xm config (danpb)
- Enable PAE with pae hvm hosts (danpb)
- Fix hvm block backed cds (danpb)
- Fix handling of block devs backed by vbds (danpb)
- Ensure we're on a xen kernel (#205889)
- Default to vncunused

* Wed Sep  6 2006 Jeremy Katz <katzj@redhat.com> - 0.92.0-2
- add patch to fix memory parsing in interactive mode
- fix deps

* Wed Aug 30 2006 Jeremy Katz <katzj@redhat.com> - 0.92.0-1
- Fix silly loop when asking about graphics support (misa)
- Fix passing macaddr
- Add support so that we reboot into the guest after installation finishes 

* Tue Aug 29 2006 Jeremy Katz <katzj@redhat.com> - 0.91.0-1
- add support for paravirt guests with framebuffer. 

* Mon Aug 21 2006 Jeremy Katz <katzj@redhat.com> - 0.90.1-1
- fix tab/space whitespace inconsistency

* Wed Aug 16 2006 Jeremy Katz <katzj@redhat.com> - 0.90.0-2
- set ExcludeArch so that it doesn't get pulled into all trees

* Wed Aug 16 2006 Jeremy Katz <katzj@redhat.com> - 0.90.0-1
- update to version with fixed HVM domain creation

* Wed Aug 16 2006 Jeremy Katz <katzj@redhat.com> - 0.9-2
- add some missing requires

* Tue Aug 15 2006 Jeremy Katz <katzj@redhat.com> - 0.9-1
- Initial build

