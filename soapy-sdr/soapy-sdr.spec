Name:           soapy-sdr
Version:        0.6.1
Release:        1%{?dist}
Summary:        Vendor and platform neutral SDR support library.

License:        Boost
URL:            https://github.com/pothosware/SoapySDR
Source0:        https://github.com/pothosware/SoapySDR/archive/soapy-sdr-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  swig

%description
SoapySDR is an open-source generalized C/C++ API and runtime library for interfacing with SDR devices.


%package libs
Summary:        Shared libraries for Soapy SDR

%description libs
Shared libraries for Soapy SDR

%package devel
Summary:        Files for development of applications which will use Soapy SDR
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development of applications which will use Soapy SDR


%package python
Summary:        Python 2 bindings for Soapy SDR
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       python2-libs

%description python


%package python3
Summary:        Python 3 bindings for Soapy SDR
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       python3-libs

%description python3


%prep
%setup -q -n SoapySDR-%{name}-%{version}


%build
mkdir build
cd build

%cmake .. \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DCMAKE_BUILD_TYPE=Release

make %{?_smp_mflags}


%install
cd build
make install DESTDIR=%{buildroot}


%check python
python2 -c "import SoapySDR; print(SoapySDR.getAPIVersion())"


%files
%{_bindir}/SoapySDRUtil
%{_mandir}/man1/SoapySDRUtil.1*
%doc LICENSE_1_0.txt Changelog.txt README.md


%files devel
%{_includedir}/SoapySDR
%{_libdir}/libSoapySDR*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake


%files libs
%{_libdir}/libSoapySDR*


%files python
%{_libdir}/python2.*/site-packages/*.so
%{_libdir}/python2.*/site-packages/*.py
%{_libdir}/python2.*/site-packages/*.pyo
%{_libdir}/python2.*/site-packages/*.pyc


%files python3
%{_libdir}/python3.*/site-packages/*.so
%{_libdir}/python3.*/site-packages/*.py
%{_libdir}/python3.*/site-packages/__pycache__/*.pyc


%changelog
* Tue Mar 20 2018 Mikkel Kroman <mk@maero.dk>
- Initial release
