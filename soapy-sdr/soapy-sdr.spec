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
%setup -n %{name}-%{version}


%build
mkdir build
cd build

%cmake .. \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DCMAKE_BUILD_TYPE=Release \

make %{?_smp_mflags}


%install
cd build
make install DESTDIR=%{buildroot}


%check python
python2 -c "import SoapySDR; print(SoapySDR.getAPIVersion())"


%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Tue Mar 20 2018 Mikkel Kroman <mk@maero.dk>
- Initial release
