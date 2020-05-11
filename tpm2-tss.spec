#
# Conditional build:
%bcond_with	gcrypt	# libgcrypt crypto instead of openssl

Summary:	OSS implementation of the TCG TPM2 Software Stack (TSS2)
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja TCG TPM2 Software Stack (TSS2)
Name:		tpm2-tss
Version:	2.4.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/tpm2-software/tpm2-tss/releases
Source0:	https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	269e8122e0588d56092abe3f2e38c8b9
URL:		https://github.com/tpm2-software/tpm2-tss
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	json-c-devel
%{?with_gcrypt:BuildRequires:	libgcrypt-devel >= 1.6.0}
BuildRequires:	libtool >= 2:2
%{!?with_gcrypt:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
%{?with_gcrypt:Requires:	libgcrypt >= 1.6.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of the Trusted Computing Group's (TCG) TPM2 Software
Stack (TSS).

%description -l pl.UTF-8
Implementacja specyfikacji TPM2 Software Stack (TSS), stworzonej przez
Trusted Computing Group (TCG).

%package devel
Summary:	Header files for tpm2-tss
Summary(es.UTF-8):	Arquivos de cabeçalho para tpm2-tss
Summary(pl.UTF-8):	Pliki nagłówkowe do tpm2-tss
Summary(pt_BR.UTF-8):	Arquivos de inclusão para a tpm2-tss
Summary(ru.UTF-8):	Хедеры для tpm2-tss
Summary(uk.UTF-8):	Хедери для tpm2-tss
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel
Requires:	json-c-devel
%{?with_gcrypt:Requires:	libgcrypt-devel >= 1.6.0}
%{!?with_gcrypt:Requires:	openssl-devel}

%description devel
Header files for implementation of the Trusted Computing Group's (TCG)
TPM2 Software Stack (TSS).

%description devel -l pl.UTF-8
Pliki nagłówkowe implementacji Trusted Computing Group (TCG) TPM2
Software Stack (TSS).

%description devel -l ru.UTF-8
Хедеры необходимые для программирования с tpm2-tss.

%description devel -l uk.UTF-8
Хедери необхідні для програмування з tpm2-tss.

%package static
Summary:	Static tpm2-tss library
Summary(es.UTF-8):	Biblioteca estática usada no desenvolvimento de aplicativos com tpm2-tss
Summary(pl.UTF-8):	Biblioteka statyczna tpm2-tss
Summary(pt_BR.UTF-8):	Biblioteca estática de desenvolvimento
Summary(ru.UTF-8):	Статическая библиотека tpm2-tss
Summary(uk.UTF-8):	Статична бібліотека tpm2-tss
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Implementation of the Trusted Computing Group's (TCG) TPM2 Software
Stack (TSS).

This package contains the static library used for development.

%description static -l pl.UTF-8
Biblioteka statyczna tpm2-tss.

%description static -l ru.UTF-8
Статическая библиотека, необходимая для программирования с tpm2-tss.

%description static -l uk.UTF-8
Статична бібліотека, необхідна для програмування з tpm2-tss.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-tmpfilesdir=%{systemdtmpfilesdir} \
	--with-udevrulesdir=/lib/udev/rules.d \
	--with-udevrulesprefix=60-

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtss2*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS README.md
%attr(755,root,root) %{_libdir}/libtss2-esys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-esys.so.0
%attr(755,root,root) %{_libdir}/libtss2-fapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-fapi.so.0
%attr(755,root,root) %{_libdir}/libtss2-mu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-mu.so.0
%attr(755,root,root) %{_libdir}/libtss2-rc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-rc.so.0
%attr(755,root,root) %{_libdir}/libtss2-sys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-sys.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-device.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-device.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-mssim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-mssim.so.0
%attr(755,root,root) %{_libdir}/libtss2-tctildr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tctildr.so.0
%dir %{_sysconfdir}/tpm2-tss
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tpm2-tss/fapi-config.json
%dir %{_sysconfdir}/tpm2-tss/fapi-profiles
%{_sysconfdir}/tpm2-tss/fapi-profiles/P_ECCP256SHA256.json
%{_sysconfdir}/tpm2-tss/fapi-profiles/P_RSA2048SHA256.json
%{systemdtmpfilesdir}/tpm2-tss-fapi.conf
/lib/udev/rules.d/60-tpm-udev.rules
# what subsystem handles this?
#/etc/sysusers.d/tpm2-tss.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtss2-esys.so
%attr(755,root,root) %{_libdir}/libtss2-fapi.so
%attr(755,root,root) %{_libdir}/libtss2-mu.so
%attr(755,root,root) %{_libdir}/libtss2-rc.so
%attr(755,root,root) %{_libdir}/libtss2-sys.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-device.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-mssim.so
%attr(755,root,root) %{_libdir}/libtss2-tctildr.so
%{_includedir}/tss2
%{_pkgconfigdir}/tss2-esys.pc
%{_pkgconfigdir}/tss2-fapi.pc
%{_pkgconfigdir}/tss2-mu.pc
%{_pkgconfigdir}/tss2-rc.pc
%{_pkgconfigdir}/tss2-sys.pc
%{_pkgconfigdir}/tss2-tcti-device.pc
%{_pkgconfigdir}/tss2-tcti-mssim.pc
%{_pkgconfigdir}/tss2-tctildr.pc
%{_mandir}/man3/ESYS_*.3*
%{_mandir}/man3/Esys_*.3*
%{_mandir}/man3/FapiTestgroup.3*
%{_mandir}/man3/Fapi_*.3*
%{_mandir}/man3/Tss2_*.3*
%{_mandir}/man7/tss2-tcti-device.7*
%{_mandir}/man7/tss2-tcti-mssim.7*
%{_mandir}/man7/tss2-tctildr.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtss2-esys.a
%{_libdir}/libtss2-fapi.a
%{_libdir}/libtss2-mu.a
%{_libdir}/libtss2-rc.a
%{_libdir}/libtss2-sys.a
%{_libdir}/libtss2-tcti-device.a
%{_libdir}/libtss2-tcti-mssim.a
%{_libdir}/libtss2-tctildr.a
