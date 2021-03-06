# -*- rpm-spec -*-

Summary: xapi - xen toolstack for XCP
Name:    xapi
Version: 1.9.20
Release: 1
Group:   System/Hypervisor
License: LGPL+linking exception
URL:  http://www.xen.org
Source0: https://github.com/djs55/xen-api/archive/%{version}/xen-api-%{version}.tar.gz
Source1: xen-api-xapi-conf
Source2: xen-api-init
Source3: xen-api-xapissl
Source4: xen-api-db-conf
Source5: xen-api-pam
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: ocaml ocaml-findlib ocaml-camlp4-devel ocaml-ocamldoc
BuildRequires: pam-devel tetex-latex ocaml xen-devel zlib-devel
BuildRequires: ocaml-xcp-idl-devel ocaml-xen-api-libs-transitional-devel
BuildRequires: ocaml-xen-api-client-devel omake ocaml-netdev-devel
BuildRequires: ocaml-cdrom-devel ocaml-fd-send-recv-devel forkexecd-devel
BuildRequires: ocaml-libvhd-devel ocaml-nbd-devel ocaml-oclock-devel
BuildRequires: ocaml-ounit-devel ocaml-rpc-devel ocaml-ssl-devel ocaml-stdext-devel
BuildRequires: ocaml-syslog-devel ocaml-tapctl-devel ocaml-xen-lowlevel-libs-devel
BuildRequires: ocaml-xenstore-devel git cmdliner-devel ocaml-xcp-inventory-devel
BuildRequires: ocaml-bitstring-devel libuuid-devel make utop
BuildRequires: ocaml-xenstore-clients-devel message-switch-devel
Requires: stunnel ocaml-xcp-inventory hwdata redhat-ls-core

%description
XCP toolstack.

%description
This package contains the xapi toolstack.

%package xe
Summary: The xapi toolstack CLI
Group: System/Hypervisor
Requires: bash-completion

%description xe
The command-line interface for controlling XCP hosts.

%package python-devel
Summary: XenAPI client support in python
Group: System/Hypervisor
Requires: python

%description python-devel
Libraries for writing XenAPI clients in python.

%prep 
%setup -q -n xen-api-%{version}
cp %{SOURCE1} xen-api-xapi-conf
cp %{SOURCE2} xen-api-init
cp %{SOURCE3} xen-api-xapissl
cp %{SOURCE4} xen-api-db-conf
cp %{SOURCE5} xen-api-pam


%build
./configure --bindir=%{_bindir} --etcdir=/etc --libexecdir=%{_libexecdir}/xapi --xapiconf=/etc/xapi.conf --hooksdir=/etc/xapi/hook-scripts --sharedir=/usr/share/xapi --plugindir=/usr/lib/xapi/plugins

export COMPILE_JAVA=no
make version
omake phase1
omake phase2
omake ocaml/xapi/xapi
omake ocaml/xe-cli/xe
omake ocaml/xapi/sparse_dd

%install
rm -rf %{buildroot}
 
mkdir -p %{buildroot}/%{_sbindir}
install -m 0755 ocaml/xapi/xapi.opt %{buildroot}/%{_sbindir}/xapi
mkdir -p %{buildroot}/etc/pam.d
install -m 0644 xen-api-pam %{buildroot}/etc/pam.d/xapi
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 0755 xen-api-init %{buildroot}%{_sysconfdir}/init.d/xapi
mkdir -p %{buildroot}/%{_libexecdir}/xapi
install -m 0755 xen-api-xapissl %{buildroot}/%{_libexecdir}/xapi/xapissl
install -m 0755 scripts/pci-info %{buildroot}/%{_libexecdir}/xapi/pci-info
install -m 0755 scripts/update-mh-info %{buildroot}/%{_libexecdir}/xapi/update-mh-info
install -m 0755 ocaml/xapi/sparse_dd %{buildroot}/%{_libexecdir}/xapi/sparse_dd
mkdir -p %{buildroot}/etc/xapi
install -m 0644 xen-api-xapi-conf %{buildroot}/etc/xapi.conf
install -m 0644 xen-api-db-conf %{buildroot}/etc/xapi/db.conf

mkdir -p %{buildroot}/%{_bindir}
install -m 0755 ocaml/xe-cli/xe.opt %{buildroot}/%{_bindir}/xe
mkdir -p %{buildroot}/etc/bash_completion.d
install -m 0755 ocaml/xe-cli/bash-completion %{buildroot}/etc/bash_completion.d/xe

mkdir -p %{buildroot}/var/lib/xapi
mkdir -p %{buildroot}/etc/xapi/hook-scripts

mkdir -p %{buildroot}/etc/xcp
echo master > %{buildroot}/etc/xcp/pool.conf

mkdir -p %{buildroot}/usr/share/xapi/packages/iso

mkdir -p %{buildroot}/usr/lib/python2.6/site-packages
install -m 0644 scripts/examples/python/XenAPI.py %{buildroot}/usr/lib/python2.6/site-packages/
install -m 0644 scripts/examples/python/XenAPIPlugin.py %{buildroot}/usr/lib/python2.6/site-packages/

%clean
rm -rf %{buildroot}

%post
[ ! -x /sbin/chkconfig ] || chkconfig --add xapi

%preun
if [ $1 -eq 0 ]; then
  /sbin/service xapi stop > /dev/null 2>&1
  /sbin/chkconfig --del xapi
fi

%files
%defattr(-,root,root,-)
%{_sbindir}/xapi
/etc/init.d/xapi
%config(noreplace) /etc/xapi.conf
%config(noreplace) /etc/xcp/pool.conf
%{_libexecdir}/xapi/xapissl
%{_libexecdir}/xapi/pci-info
%{_libexecdir}/xapi/update-mh-info
%{_libexecdir}/xapi/sparse_dd
/etc/xapi/db.conf
/etc/xapi/hook-scripts
/var/lib/xapi
/usr/share/xapi/packages/iso
/etc/pam.d/xapi

%files xe
%defattr(-,root,root,-)
%{_bindir}/xe
/etc/bash_completion.d/xe

%files python-devel
%defattr(-,root,root,-)
/usr/lib/python2.6/site-packages/XenAPI.py
/usr/lib/python2.6/site-packages/XenAPI.pyo
/usr/lib/python2.6/site-packages/XenAPI.pyc

/usr/lib/python2.6/site-packages/XenAPIPlugin.py
/usr/lib/python2.6/site-packages/XenAPIPlugin.pyo
/usr/lib/python2.6/site-packages/XenAPIPlugin.pyc

%changelog
* Mon Sep  1 2013 David Scott <dave.scott@eu.citrix.com> - 1.9.20-1
- Fix XenAPI.py on python2.7

* Tue Aug 20 2013 David Scott <dave.scott@eu.citrix.com> - 1.9.19-1
- Add sparse_dd to the xapi package so VDI.copy should work

* Tue Jun 18 2013 David Scott <dave.scott@eu.citrix.com> - 1.9.6-1
- Update to 1.9.6

* Sun Jun 8 2013 David Scott <dave.scott@eu.citrix.com> - 1.9.2-1
- Add python-devel for writing python clients

* Wed Jun 5 2013 David Scott <dave.scott@eu.citrix.com> - 1.9.1-1
- Initial package






