%define oname	kvirc

%define svn	2253
%define rel	1

%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%{oname}-%{svn}.tar.lzma
%define dirname		%{oname}
%else
%define release		%mkrel %rel
%define distname	%{oname}-%{version}.tar.bz2
%define dirname		%{oname}-%{version}
%endif

%define major		4
%define libname		%mklibname kvilib4_ %major
%define develname	%mklibname kvilib4 -d

Name:		kvirc4
Version:	4.0.0
Release:	%{release}
Summary:	Qt IRC client
Group:		Networking/IRC
License:	GPLv2+
URL:		http://www.kvirc.net
Source:		%{distname}
BuildRoot:	%{_tmppath}/%{oname}-%{version}-%{release}
BuildRequires:	qt4-devel
BuildRequires:	kdelibs4-devel
BuildRequires:	perl-devel
BuildRequires:	gettext
Requires:	kvirc-icons

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%package -n kvirc-icons
Summary:	Icons for KVirc
Group:		Networking/IRC

%description -n kvirc-icons
This package contains icons for KVirc. It is a separate package so
multiple versions of KVirc can be packaged without conflicting.

%package -n %{libname}
Summary:	Shared library for KVirc 4
Group:		System/Libraries

%description -n %{libname}
Shared library provided by KVirc 4.

%package -n %{develname}
Requires:	%{libname} = %{version}-%{release}
Summary:	Development headers for KVirc 4
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname kvirc 3 -d} < %{version}-%{release}

%description -n %{develname}
Development headers for KVirc 4.

%prep 
%setup -q -n %{dirname}

%build
# To avoid any possible occurrence of the OpenSSL / GPL license issue
# - AdamW 2008/08
%cmake -DWITH_KDE4=true -DWITHOUT_SSL=true
%make

%install
rm -rf %{buildroot}
pushd build
%makeinstall_std
popd

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,scalable}/apps
for i in 16x16 32x32 48x48 64x64 128x128 scalable; do \
	cp data/icons/$i/*.* %{buildroot}%{_iconsdir}/hicolor/$i/apps; \
done
rm -f %{buildroot}%{_iconsdir}/hicolor/scalable/apps/createpng.sh

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{oname}/4.0
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mimelnk/*/*.desktop

%files -n kvirc-icons
%{_iconsdir}/hicolor/*/apps/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libkvilib4.so.%{major}*

%files  -n %{develname}
%defattr(-,root,root)
%{_libdir}/libkvilib4.so

