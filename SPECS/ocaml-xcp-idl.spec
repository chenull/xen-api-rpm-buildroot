Name:           ocaml-xcp-idl
Version:        0.9.11
Release:        1
Summary:        Common interface definitions for XCP services
License:        LGPL
Group:          Development/Other
URL:            https://github.com/xapi-project/xcp-idl/archive/%{version}.tar.gz
Source0:        https://github.com/xapi-project/xcp-idl/archive/%{version}/xcp-idl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml ocaml-findlib ocaml-camlp4-devel
BuildRequires:  ocaml-cohttp-devel xmlm-devel ocaml-rpc-devel ocaml-syslog-devel message-switch-devel cmdliner-devel ocaml-fd-send-recv-devel ocaml-xcp-rrd-devel
BuildRequires:  ocaml-ounit-devel

# XXX transitive dependencies of message-switch-devel
BuildRequires: ocaml-oclock-devel

#  "uri"
#"re"
#           "cohttp"
#           "xmlm"
#           "rpc" {> "1.4.0"}
#           "ocamlfind"
#           "syslog"
#           "message_switch"
Requires:       ocaml ocaml-findlib

%description
Common interface definitions for XCP services.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
#Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n xcp-idl-%{version}

%build
ocaml setup.ml -configure --destdir %{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -install

%clean
rm -rf %{buildroot}

%files
#This space intentionally left blank

%files devel
%defattr(-,root,root)
%doc LICENSE README.md ChangeLog MAINTAINERS
%{_libdir}/ocaml/xcp/*

%changelog
* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

