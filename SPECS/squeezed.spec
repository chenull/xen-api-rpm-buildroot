Name:           squeezed
Version:        0.10.0
Release:        1
Summary:        Memory ballooning daemon for the xapi toolstack
License:        LGPL
Group:          Development/Other
URL:            https://github.com/xapi-project/squeezed/archive/%{version}.tar.gz
Source0:        https://github.com/xapi-project/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        squeezed-init
Source2:        squeezed-conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml ocaml-obuild ocaml-findlib ocaml-camlp4-devel
BuildRequires:  ocaml-stdext-devel ocaml-xcp-idl-devel ocaml-syslog-devel
BuildRequires:  ocaml-xen-lowlevel-libs-devel ocaml-xenstore-devel ocaml-xenstore-clients-devel
BuildRequires:  ocaml-rpc-devel
BuildRequires:  ocaml-re-devel ocaml-cohttp-devel
BuildRequires:  ocaml-oclock-devel xen-devel
Requires:       xen-libs redhat-lsb-core

%description
Memory ballooning daemon for the xapi toolstack.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} squeezed-init
cp %{SOURCE2} squeezed-conf

%build
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_sbindir}
install dist/build/squeezed/squeezed %{buildroot}/%{_sbindir}/squeezed
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 0755 squeezed-init %{buildroot}%{_sysconfdir}/init.d/squeezed
mkdir -p %{buildroot}/etc
install -m 0644 squeezed-conf %{buildroot}%{_sysconfdir}/squeezed.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md LICENSE MAINTAINERS
%{_sbindir}/squeezed
%{_sysconfdir}/init.d/squeezed
%{_sysconfdir}/squeezed.conf

%post
/sbin/chkconfig --add squeezed

%preun
if [ $1 -eq 0 ]; then
  /sbin/service squeezed stop > /dev/null 2>&1
  /sbin/chkconfig --del squeezed
fi

%changelog
* Mon Sep  2 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.10.0, with support for domain 0 ballooning

* Wed Jun  5 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

