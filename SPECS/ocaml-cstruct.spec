Name:           ocaml-cstruct
Version:        0.7.1
Release:        1
Summary:        Read and write low-level C-style structures in OCaml
License:        ISC
Group:          Development/Other
URL:            https://github.com/mirage/ocaml-cstruct/archive/ocaml-cstruct-0.7.1.tar.gz
Source0:        https://github.com/mirage/%{name}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml ocaml-findlib ocaml-ocplib-endian-devel ocaml-camlp4 ocaml-camlp4-devel
Requires:       ocaml ocaml-findlib ocaml-ocplib-endian-devel
#XXX ocaml-cstruct should require caml-ocplib-endian, not -devel

%description
Read and write low-level C-style structures in OCaml.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
ocaml setup.ml -configure --destdir %{buildroot}/%{_libdir}/ocaml
ocaml setup.ml -build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/ocaml
mkdir -p %{buildroot}/%{_libdir}/ocaml/stublibs

export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_LDCONF=ignore
ocaml setup.ml -install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
# This space intentionally left blank

%files devel
%defattr(-,root,root)
%doc README.md CHANGES
%{_libdir}/ocaml/cstruct/*
%{_libdir}/ocaml/stublibs/dllcstruct_stubs.so
%{_libdir}/ocaml/stublibs/dllcstruct_stubs.so.owner

%changelog
* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

