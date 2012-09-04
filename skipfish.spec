%define		subver	b
%define		rel	2
Summary:	Web application security scanner
Name:		skipfish
Version:	2.09
Release:	0.%{subver}.%{rel}
License:	Apache v2.0
Group:		Applications/Networking
Source0:	http://skipfish.googlecode.com/files/%{name}-%{version}%{subver}.tgz
# Source0-md5:	9fb6e388a2fa462e84496d3a4c3c198e
URL:		http://code.google.com/p/skipfish/
BuildRequires:	libidn-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A fully automated, active web application security reconnaissance
tool.

Key features:
- High speed: pure C code, highly optimized HTTP handling, minimal CPU
  footprint - easily achieving 2000 requests per second with responsive
  targets.
- Ease of use: heuristics to support a variety of quirky web
  frameworks and mixed-technology sites, with automatic learning
  capabilities, on-the-fly wordlist creation, and form autocompletion.
- Cutting-edge security logic: high quality, low false positive,
  differential security checks, capable of spotting a range of subtle
  flaws, including blind injection vectors.

%prep
%setup -q -n %{name}-%{version}%{subver}

%{__sed} -i -e 's,-O3,$(OPTCFLAGS),' Makefile
%{__sed} -i -e 's,-L/usr/local/lib/ -L/opt/local/lib,$(OPTLDFLAGS),' Makefile
%{__sed} -i -e 's,"assets","%{_datadir}/%{name}/assets",' src/config.h
%{__sed} -i -e 's,"signatures/,"%{_sysconfdir}/%{name}/,' src/config.h
%{__sed} -i -e 's,signatures/,%{_datadir}/%{name}/signatures/,' signatures/signatures.conf

%build
%{__make} \
	CC="%{__cc}" \
	OPTCFLAGS="%{rpmcflags} %{rpmcppflags}" \
	OPTLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/%{name},%{_datadir}/%{name}/{,signatures},%{_mandir}/man1}

install -p %{name} $RPM_BUILD_ROOT%{_bindir}
cp -a doc/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a signatures/signatures.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -ar assets dictionaries $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -ar signatures/*.sigs $RPM_BUILD_ROOT%{_datadir}/%{name}/signatures

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README doc/*.txt
%attr(755,root,root) %{_bindir}/skipfish
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/signatures.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/assets
%{_datadir}/%{name}/dictionaries
%{_datadir}/%{name}/signatures
%{_mandir}/man1/%{name}.1*
