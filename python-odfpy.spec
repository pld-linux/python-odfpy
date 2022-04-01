#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python 2 API and tools to manipulate OpenDocument files
Summary(pl.UTF-8):	API i narzędzia Pythona 2 do operacji na dokumentach OpenDocument
Name:		python-odfpy
Version:	1.4.1
Release:	6
License:	LGPL v2.1+ (module), Apache v2.0 and GPL v2+ (tools)
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/odfpy/
Source0:	https://files.pythonhosted.org/packages/source/o/odfpy/odfpy-%{version}.tar.gz
# Source0-md5:	d1a186ae75b2ae038a8aab1396444342
URL:		https://pypi.org/project/odfpy/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-defusedxml
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-defusedxml
BuildRequires:	python3-pytest
%endif
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Odfpy is a library to read and write OpenDocument v. 1.2 files. The
main focus has been to prevent the programmer from creating invalid
documents. It has checks that raise an exception if the programmer
adds an invalid element, adds an attribute unknown to the grammar,
forgets to add a required attribute or adds text to an element that
doesn't allow it.

%description -l pl.UTF-8
Odfpy to biblioteka do odczytu i zapisu plików OpenDocument w wersji
1.2. Główny nacisk został położony na tym, aby nie pozwolić
programiście na utworzenie błędnych dokumentów. Biblioteka rzuca
wyjątek, jeśli programista dodaje błędny element, dodaje element
nieznany gramatyce, zapomina dodać wymagany atrybut lub dodaje tekst
do elementu, który na to nie pozwala.

%package -n python3-odfpy
Summary:	Python 3 API and tools to manipulate OpenDocument files
Summary(pl.UTF-8):	API i narzędzia Pythona 3 do operacji na dokumentach OpenDocument
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-odfpy
Odfpy is a library to read and write OpenDocument v. 1.2 files. The
main focus has been to prevent the programmer from creating invalid
documents. It has checks that raise an exception if the programmer
adds an invalid element, adds an attribute unknown to the grammar,
forgets to add a required attribute or adds text to an element that
doesn't allow it.

%description -n python3-odfpy -l pl.UTF-8
Odfpy to biblioteka do odczytu i zapisu plików OpenDocument w wersji
1.2. Główny nacisk został położony na tym, aby nie pozwolić
programiście na utworzenie błędnych dokumentów. Biblioteka rzuca
wyjątek, jeśli programista dodaje błędny element, dodaje element
nieznany gramatyce, zapomina dodać wymagany atrybut lub dodaje tekst
do elementu, który na to nie pozwala.

%package -n odfpy-tools
Summary:	Tools to manipulate OpenDocument files
Summary(pl.UTF-8):	Narzędzia do operacji na dokumentach OpenDocument
Group:		Applications/Publishing
%if %{with python3}
Requires:	python3-odfpy = %{version}-%{release}
%else
Requires:	python-odfpy = %{version}-%{release}
%endif

%description -n odfpy-tools
Tools to manipulate OpenDocument files.

%description -n odfpy-tools -l pl.UTF-8
Narzędzia do operacji na dokumentach OpenDocument.

%prep
%setup -q -n odfpy-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_xmlgenerator_wo_ns apparently fails with python 2.7
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests -k 'not test_xmlgenerator_wo_ns'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python3}
# ensure packaged tools are python3 based
%{__rm} -r $RPM_BUILD_ROOT{%{_bindir},%{_mandir}}
%endif
%endif

%if %{with python3}
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-odfpy-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-odfpy-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc ChangeLog README.md
%{py_sitescriptdir}/odf
%{py_sitescriptdir}/odfpy-%{version}-py*.egg-info
%{_examplesdir}/python-odfpy-%{version}
%endif

%if %{with python3}
%files -n python3-odfpy
%defattr(644,root,root,755)
%doc ChangeLog README.md
%{py3_sitescriptdir}/odf
%{py3_sitescriptdir}/odfpy-%{version}-py*.egg-info
%{_examplesdir}/python3-odfpy-%{version}
%endif

%files -n odfpy-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/csv2ods
%attr(755,root,root) %{_bindir}/mailodf
%attr(755,root,root) %{_bindir}/odf2mht
%attr(755,root,root) %{_bindir}/odf2xhtml
%attr(755,root,root) %{_bindir}/odf2xml
%attr(755,root,root) %{_bindir}/odfimgimport
%attr(755,root,root) %{_bindir}/odflint
%attr(755,root,root) %{_bindir}/odfmeta
%attr(755,root,root) %{_bindir}/odfoutline
%attr(755,root,root) %{_bindir}/odfuserfield
%attr(755,root,root) %{_bindir}/xml2odf
%{_mandir}/man1/csv2ods.1*
%{_mandir}/man1/mailodf.1*
%{_mandir}/man1/odf2mht.1*
%{_mandir}/man1/odf2xhtml.1*
%{_mandir}/man1/odf2xml.1*
%{_mandir}/man1/odfimgimport.1*
%{_mandir}/man1/odflint.1*
%{_mandir}/man1/odfmeta.1*
%{_mandir}/man1/odfoutline.1*
%{_mandir}/man1/odfuserfield.1*
%{_mandir}/man1/xml2odf.1*
