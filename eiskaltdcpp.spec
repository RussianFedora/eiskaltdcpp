Name:       eiskaltdcpp
Version:    2.2.6
Release:    4%{?dist}
Summary:    QT Direct Connect client
Summary(ru):Клиент сети Direct Connect на QT

License:    GPLv3
Group:      Applications/Internet
URL:        http://code.google.com/p/eiskaltdc
Source0:    http://eiskaltdc.googlecode.com/files/%{name}-%{version}.tar.xz
Source100:  README.RFRemix
Patch0:     eiskaltdcpp-gcc47.patch

BuildRequires:  cmake >= 2.6.3
BuildRequires:  boost-devel
BuildRequires:  aspell-devel
BuildRequires:  libupnp-devel
BuildRequires:  qt-devel >= 4.4.0
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  gettext-devel
BuildRequires:  gtk3-devel
BuildRequires:  libnotify-devel
BuildRequires:  lua-devel
BuildRequires:  libglade2-devel
BuildRequires:  libidn-devel

Requires:       %{name}-gui = %{version}-%{release}


%description
EiskaltDC++ is a program the uses the Direct Connect protocol. It is compatible
with other DC clients, such as the original DC from Neomodus, DC++ and
derivatives. EiskaltDC++ also interoperates with all common DC hub software.

%description -l ru
EiskaltDC++ использует протокол Direct Connect. Программа совместима с другими
клиентами DC, так же как и с оригинальным DC от Neomodus, с DC++ и
производными. EiskaltDC++ also взаимодействует со всем обычным ПО хабов DC

%package gtk
Group:      Applications/Internet
Summary:    GTK-based graphical interface
Summary(ru):Графический интерфейс GTK
Provides:   %{name}-gui = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

%description gtk
Gtk interface based on code of FreeDC++ and LinuxDC++

%description gtk -l ru
Gtk интерфейс основанный на коде FreeDC++ и LinuxDC++


%package qt
Group:      Applications/Internet
Summary:    Qt-based graphical interface
Summary(ru):Графический интерфейс QT
Provides:   %{name}-gui = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}

%description qt
Qt-based graphical interface

%description qt -l ru
Интерфейс QT для %{name}

%prep
%setup -q
%patch0 -p1 -b .gcc47

%build
rm -rf examples/*.php eiskaltdcpp-qt/qtscripts/gnome/*.php
%cmake \
    -DUSE_ASPELL=ON \
    -DUSE_QT=ON \
    -DFREE_SPACE_BAR_C=ON \
    -DUSE_MINIUPNP=ON \
    -DLOCAL_MINIUPNP=ON \
    -DUSE_GTK3=ON \
    -DDBUS_NOTIFY=ON \
    -DUSE_JS=ON \
    -DWITH_LUASCRIPTS=ON

make %{?_smp_mflags}
cp %{SOURCE100} .


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/%{name}/examples/*.php

%find_lang %{name}-gtk
%find_lang lib%{name}


%clean
rm -rf %{buildroot}


%files -f lib%{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.RFRemix
%{_datadir}/eiskaltdcpp/emoticons
%{_datadir}/eiskaltdcpp/examples
%{_libdir}/libeiskaltdcpp.so.*
%{_datadir}/icons/hicolor/*/apps/eiskaltdcpp.png
%{_datadir}/pixmaps/*.png


%files gtk -f %{name}-gtk.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/*gtk
%{_mandir}/man?/*gtk*
%{_datadir}/eiskaltdcpp/gtk/*
%{_datadir}/applications/*gtk*.desktop


%files qt
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/*qt
%{_mandir}/man?/*qt*
%{_datadir}/eiskaltdcpp/qt/*
%{_datadir}/applications/*qt*.desktop
%{_datadir}/eiskaltdcpp/update_geoip


%changelog
* Thu Apr 13 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-4.R
- Added patch for compile with gcc 4.7

* Thu Mar 21 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-3.R
- Switch to GTK3 interface

* Tue Feb 21 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-2.R
- Back to GTK2 interface

* Tue Feb 21 2012 Vasiliy N. Glazov <vascom2@gmail.com> 2.2.6-1.R
- Update to 2.2.6

* Tue Dec 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.5-2.R
- Removed php

* Mon Dec 26 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.5-2.R
- Update to 2.2.5

* Tue Nov 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.4-2.R
- Added description in russian language

* Mon Oct 03 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 2.2.4-1.R
- Update to 2.2.4

* Mon Jun 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.3-1.R
- update to 2.2.3

* Mon Apr 25 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 2.2.2-1.R
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

* Mon Jan  3 2007 Luke Macken <lmacken@redhat.com> 0.3.8-1
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

* Tue Oct 03 2005 Luke Macken <lmacken@redhat.com> 0.3.7-4
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
