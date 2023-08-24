#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kdebugsettings
Summary:	Kdebugettings
Name:		ka5-%{kaname}
Version:	23.08.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	0e5e12af0f9334b95aaab2fc095f4cf4
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-kcompletion-devel >= %{kframever}
BuildRequires:	kf5-kconfig-devel >= %{kframever}
BuildRequires:	kf5-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf5-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kitemviews-devel >= %{kframever}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An application to enable/disable qCDebug.

%description -l pl.UTF-8
Program do włączania/wyłączania qCDebug.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kdebugsettings
%{_desktopdir}/org.kde.kdebugsettings.desktop
%{_datadir}/qlogging-categories5/kde.renamecategories
%{_datadir}/qlogging-categories5/kdebugsettings.categories
%attr(755,root,root) %{_libdir}/libkdebugsettings.so.*.*.*
%ghost %{_libdir}/libkdebugsettings.so.5
%attr(755,root,root) %{_libdir}/libkdebugsettingscore.so.*.*.*
%ghost %{_libdir}/libkdebugsettingscore.so.5
%{_datadir}/metainfo/org.kde.kdebugsettings.appdata.xml
%{_datadir}/kdebugsettings
