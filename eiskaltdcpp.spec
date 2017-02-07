%global gitcommit_full 0fa9a730eb63ba1a4f9440d5a746e8d6df094286
%global gitcommit %(c=%{gitcommit_full}; echo ${c:0:7})
%global date 20161119

Name:           eiskaltdcpp
Version:        2.2.11
Release:        0.%{date}git%{gitcommit}%{dist}
Summary:        Direct Connect client
Summary(ru):    Клиент сети Direct Connect

License:        GPLv3+
URL:            https://github.com/eiskaltdcpp/eiskaltdcpp
Source0:        %{url}/tarball/%{gitcommit_full}
Patch0:         %{name}-openssl11.patch

BuildRequires:  cmake >= 2.6.3
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(aspell)
BuildRequires:  pkgconfig(libupnp)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Declarative)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(libglade-2.0)
BuildRequires:  pkgconfig(libidn)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  miniupnpc-devel

Requires:       hicolor-icon-theme

Provides:       perl(cli-xmlrpc-config.pl) = 0.1


%description
EiskaltDC++ is a program the uses the Direct Connect protocol. It is compatible
with other DC clients, such as the original DC from Neomodus, DC++ and
derivatives. EiskaltDC++ also interoperates with all common DC hub software.

%description -l ru
EiskaltDC++ использует протокол Direct Connect. Программа совместима с другими
клиентами DC, так же как и с оригинальным DC от Neomodus, с DC++ и
производными. EiskaltDC++ взаимодействует со всем обычным ПО хабов DC.

%package gtk
Summary:    GTK-based graphical interface
Summary(ru):Графический интерфейс GTK
Requires:   %{name}%{?_isa} = %{version}-%{release}
Provides:   %{name}-gui%{?_isa} = %{version}-%{release}

%description gtk
GTK+ 3 interface using GTK+ 3 library.

%description gtk -l ru
GTK+ 3 интерфейс с использование библиотеки GTK+ 3.


%package qt
Summary:    Qt-based graphical interface
Summary(ru):Графический интерфейс Qt
Requires:   %{name}%{?_isa} = %{version}-%{release}
Provides:   %{name}-gui%{?_isa} = %{version}-%{release}

%description qt
Qt-based graphical interface.

%description qt -l ru
Интерфейс Qt для %{name}.

%prep
%autosetup -p1 -n %{name}-%{name}-%{gitcommit}

# Remove bundled libs
rm -rf json upnp
rm -rf data/examples/*.php eiskaltdcpp-qt/qtscripts/gnome/*.php
# Correct rpmlint W: crypto-policy-non-compliance-openssl
sed -i -e 's/, ciphersuites/, "PROFILE=SYSTEM"/g' dcpp/CryptoManager.cpp

%build
%cmake \
    -DUSE_ASPELL=ON \
    -DUSE_QT_QML=ON \
    -DFREE_SPACE_BAR_C=ON \
    -DUSE_MINIUPNP=ON \
    -DUSE_GTK3=ON \
    -DDBUS_NOTIFY=ON \
    -DUSE_JS=ON \
    -DPERL_REGEX=ON \
    -DUSE_CLI_XMLRPC=ON \
    -DWITH_SOUNDS=ON \
    -DLUA_SCRIPT=ON \
    -DWITH_LUASCRIPTS=ON

%make_build


%install
%make_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%find_lang %{name}-gtk
%find_lang lib%{name}

%post -p /sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -p /sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f lib%{name}.lang
%doc AUTHORS ChangeLog.txt README.md TODO
%license COPYING LICENSE
%{_bindir}/%{name}-cli-xmlrpc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/cli/cli-xmlrpc-config.pl
%{_datadir}/%{name}/luascripts
%{_datadir}/%{name}/emoticons
%{_datadir}/%{name}/examples
%{_datadir}/%{name}/sounds
%{_libdir}/libeiskaltdcpp.so.*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/*.png
%{_mandir}/man?/%{name}-cli-xmlrpc.1.*


%files gtk -f %{name}-gtk.lang
%{_bindir}/*gtk
%{_mandir}/man?/*gtk*
%{_datadir}/%{name}/gtk
%{_datadir}/applications/*gtk*.desktop


%files qt
%{_bindir}/*qt
%{_mandir}/man?/*qt*
%{_datadir}/%{name}/qt
%{_datadir}/applications/*qt*.desktop
%{_datadir}/%{name}/update_geoip


%changelog
* Tue Feb 07 2017 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.11-0.20161119git0fa9a73
- Update to last git version
- Add scriptlet for icons
- Add patch for openssl 1.1.0

* Tue Aug 16 2016 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.11-0.20160510git52af555
- Clean spec
- Switch to git version

* Fri Jun 24 2016 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.10-2
- Rebuild for new boost

* Mon Sep 28 2015 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.10-1
- Update to 2.2.10

* Thu May 14 2015 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.9-7
- Bump rebuild for Fedora 22
- Change URL to Sourceforge

* Wed Oct 08 2014 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.9-6
- Bump rebuild for Fedora 21

* Mon Apr 28 2014 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.9-5
- Rebuild
- Correct provides

* Mon Nov 25 2013 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.9-3
- Use multiple licenses
- Remove bundled libs

* Fri Nov 22 2013 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.9-2
- Clean spec and descriptions
- Enable cli-xmlrpc
- License corrected

* Fri Aug 30 2013 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.9-1
- Update to 2.2.9

* Mon Jun 24 2013 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.8-1
- Update to 2.2.8

* Tue May 07 2013 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.7-2
- Rebuild for F19

* Thu May 31 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.7-1
- Update to 2.2.7

* Sat May 12 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-5
- Added patch for non segfault in QT

* Fri Apr 13 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-4
- Added patch for compile with gcc 4.7

* Wed Mar 21 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-3
- Switch to GTK3 interface

* Tue Feb 21 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-2
- Back to GTK2 interface

* Tue Feb 21 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-1
- Update to 2.2.6

* Tue Dec 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.5-2
- Removed php

* Mon Dec 26 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.5-2
- Update to 2.2.5

* Tue Nov 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.4-2
- Added description in russian language

* Mon Oct 03 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.4-1
- Update to 2.2.4

* Mon Jun 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.3-1
- update to 2.2.3

* Mon Apr 25 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.2-1
- update to 2.2.2
- added BR: libidn-devel

* Wed Mar  9 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.1-1
- update to 2.2.1

* Mon Jan 17 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.0-1
- update to 2.2.0

* Wed Dec  1 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.1.1-1
- update to 2.1.1

* Wed Nov 10 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.1.0-1
- update to 2.1.0
- added BR: gettext-devel gtk2-devel libnotify-devel lua-devel
  libglade2-devel
- build with gtk+
- make separate packages for gtk and qt gui

* Tue Oct 19 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.0.3-2
- remove php xamples

* Mon Oct 18 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.0.3-1
- update to 2.0.3

* Wed May 12 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.0.2-1
- update to new cpp version 2.0.2

* Thu Oct 29 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 1.0.30-1
- update to 1.0.30

* Mon Sep 28 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 1.0.2-1
- update to 1.0.2

* Wed Aug 26 2009 Dmitriy Pomerantsev (pda) <lrngate@yandex.ru> 1.0.0-1
- 1.0.0 from new upstream
- spec file is updated to Fedora standards

* Wed Jan 10 2007 Edward Sheldrake <ejs1920@yahoo.co.uk> 0.3.8-1
- replace antique .spec.in with one based on Fedora Extras .spec
- remove extra desktop file and icon sources

* Wed Jan 03 2007 Luke Macken <lmacken@redhat.com> 0.3.8-1
- 0.3.8 from new upstream
- Remove valknut-0.3.7-extra-qualification.patch

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> 0.3.7-9
- Rebuild for FC6

* Sun Apr 30 2006 Luke Macken <lmacken@redhat.com> 0.3.7-8
- Execute with --disable-tray in desktop file, since it is horribly broken.

* Tue Feb 28 2006 Luke Macken <lmacken@redhat.com> 0.3.7-7
- Add patch to remove extra qualification build error

* Wed Feb 15 2006 Luke Macken <lmacken@redhat.com> 0.3.7-6
- Rebuild for FE5

* Wed Nov 09 2005 Luke Macken <lmacken@redhat.com> 0.3.7-5
- Rebuild for new openssl

* Mon Oct 03 2005 Luke Macken <lmacken@redhat.com> 0.3.7-4
- Add openssl-devel to BuildRequires

* Mon Oct 03 2005 Luke Macken <lmacken@redhat.com> 0.3.7-3
- Add bzip2-devel to BuildRequires

* Mon Oct 03 2005 Luke Macken <lmacken@redhat.com> 0.3.7-2
- Requires desktop-file-utils
- Use environment variables instead of hardcoding QTDIR
- Remove duplicate category from desktop file
- Use -p when calling 'install'

* Thu Sep 29 2005 Luke Macken <lmacken@redhat.com> 0.3.7-1
- Packaged for Fedora Extras
