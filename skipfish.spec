%define		subver	b
%define		rel		1
Summary:	Web application security scanner
Name:		skipfish
Version:	1.70
Release:	0.%{subver}.%{rel}
License:	Apache v2.0
Group:		Applications/Networking
Source0:	http://skipfish.googlecode.com/files/%{name}-%{version}%{subver}.tgz
# Source0-md5:	94c946e51160e7ee24a0e2f2cbe599a4
URL:		http://code.google.com/p/skipfish/
BuildRequires:	libidn-devel
BuildRequires:	openssl-devel
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

%build
%{__make} \
	CC="%{__cc}" \
	OPTCFLAGS="%{rpmcflags}" \
	OPTLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/skipfish
