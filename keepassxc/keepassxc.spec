Name:           keepassxc
Version:        2.3.1
Release:        3%{?dist}
Summary:        Cross-platform password manager
License:        Boost and BSD and CC0 and GPLv3 and LGPLv2 and LGPLv2+ and LGPLv3+ and Public Domain
URL:            http://www.keepassxc.org/
Source0:     	https://github.com/keepassxreboot/keepassxc/releases/download/%{version}/keepassxc-%{version}-src.tar.xz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel >= 5.2
BuildRequires:  qt5-qttools-devel >= 5.2
BuildRequires:  libgcrypt-devel >= 1.6
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libXi-devel
BuildRequires:  libXtst-devel
BuildRequires:  libyubikey-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  ykpers-devel
BuildRequires:  zlib-devel
BuildRequires:  libappstream-glib
BuildRequires:  libargon2-devel
BuildRequires:  libcurl-devel
BuildRequires:  libsodium-devel

%description
KeePassXC is a community fork of KeePassX
KeePassXC is an application for people with extremely high demands on secure
personal data management.
KeePassXC saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassXC offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe.



%prep
%setup -n %{name}-%{version}

# get rid of icon tag in appdata file
# icon tag is not allowed in desktop appdata file
sed -i '/\<icon/d' share/linux/org.%{name}.KeePassXC.appdata.xml


%build
mkdir build
cd build

%cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_VERBOSE_MAKEFILE=OFF \
    -DWITH_TESTS=OFF \
    -DWITH_XC_ALL=ON \
    -DCMAKE_BUILD_TYPE=Release
 
make %{?_smp_mflags}
 
%install
cd build
make install DESTDIR=%{buildroot}
 
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    --delete-original \
    --add-mime-type application/x-keepassxc \
    %{buildroot}%{_datadir}/applications/org.%{name}.KeePassXC.desktop
 
# Associate KDB* files
cat > x-keepassxc.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassxc.png
MimeType=application/x-keepassxc
Patterns=*.kdb;*.KDB;*.kdbx;*.KDBX*
Type=MimeType
EOF
install -D -m 644 -p x-keepassxc.desktop \
    %{buildroot}%{_datadir}/mimelnk/application/x-keepassxc.desktop

#install appdata files
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/org.%{name}.KeePassXC.appdata.xml

%find_lang keepassx --with-qt

%check
ctest -V %{?_smp_mflags}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null ||:
 
%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
desktop-file-validate %{_datadir}/applications/keepassxc.desktop &> /dev/null || :

%files
%doc README.md
%license COPYING LICENSE*
%{_bindir}/keepassxc
%{_bindir}/keepassxc-cli
%{_bindir}/keepassxc-proxy
%{_datadir}/keepassxc
%{_datadir}/applications/org.%{name}.KeePassXC.desktop
%{_datadir}/metainfo/org.%{name}.KeePassXC.appdata.xml
%{_datadir}/mimelnk
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/*/*keepassxc*
%{_libdir}/%{name}
%{_mandir}/man1/keepassxc-cli.1.gz

%changelog
* Wed Mar 07 2018 Mikkel Kroman <mk@maero.dk> - 2.3.1-3
- Added libcurl-devel, libargon2-devel and libsodium-devel to BuildRequires
- Updated to version 2.3.1

* Wed Dec 27 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.4-3
- Fix specfile error

* Sat Dec 16 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.4-2
- Adjust for changes in appdata and desktop filename change

* Thu Dec 14 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.4-1
- 2.2.4 release
- removed patch to fix typo in a XML tag

* Tue Dec 12 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.3-1
- 2.2.3 release
- added patch to fix typo in a XML tag

* Sun Oct 22 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2
- Fix desktop file names
- Added BR on libappstream-glib
- Install appdata file

* Mon Oct 02 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.1-1
- 2.2.1 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.0-1
- 2.2.0 release
- added %{_bindir}/keepassxc-cli
- changed -DWITH_XC_YUBIKEY=OFF to -DWITH_XC_YUBIKEY=ON
- added BuildRequires: ykpers-devel and BuildRequires: libyubikey-devel

* Fri May 19 2017 Germano Massullo <germano.massullo@gmail.com> - 2.1.4-2
- Disabled Yubikey support. It will be re-enabled on 2.2.0 release

* Sun May 14 2017 Germano Massullo <germano.massullo@gmail.com> - 2.1.4-1
- First release on Fedora repository
