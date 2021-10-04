#
# Conditional build:
%bcond_with	mbedtls	# mbedTLS crypto instead of OpenSSL

Summary:	OSS implementation of the TCG TPM2 Software Stack (TSS2)
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja TCG TPM2 Software Stack (TSS2)
Name:		tpm2-tss
Version:	3.1.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/tpm2-software/tpm2-tss/releases
Source0:	https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4d04cf52fff4ee061bb3f7b4f4ea03b7
Patch0:		%{name}-install.patch
URL:		https://github.com/tpm2-software/tpm2-tss
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	json-c-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 2:2
%{?with_mbedtls:BuildRequires:	mbedtls-devel}
%{!?with_mbedtls:BuildRequires:	openssl-devel >= 0.9.8}
BuildRequires:	pkgconfig
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
%{?with_mbedtls:Requires:	mbedtls-devel >= 1.6.0}
%{!?with_mbedtls:Requires:	openssl-devel >= 0.9.8}

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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_mbedtls:--with-crypto=mbed} \
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
%doc AUTHORS CHANGELOG.md LICENSE MAINTAINERS README.md
%attr(755,root,root) %{_libdir}/libtss2-esys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-esys.so.0
%attr(755,root,root) %{_libdir}/libtss2-fapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-fapi.so.1
%attr(755,root,root) %{_libdir}/libtss2-mu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-mu.so.0
%attr(755,root,root) %{_libdir}/libtss2-rc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-rc.so.0
%attr(755,root,root) %{_libdir}/libtss2-sys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-sys.so.1
%attr(755,root,root) %{_libdir}/libtss2-tcti-cmd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-cmd.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-device.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-device.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-mssim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-mssim.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-pcap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-pcap.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-swtpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-swtpm.so.0
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
%{_mandir}/man5/fapi-config.5*
%{_mandir}/man5/fapi-profile.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtss2-esys.so
%attr(755,root,root) %{_libdir}/libtss2-fapi.so
%attr(755,root,root) %{_libdir}/libtss2-mu.so
%attr(755,root,root) %{_libdir}/libtss2-rc.so
%attr(755,root,root) %{_libdir}/libtss2-sys.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-cmd.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-device.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-mssim.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-pcap.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-swtpm.so
%attr(755,root,root) %{_libdir}/libtss2-tctildr.so
%{_includedir}/tss2
%{_pkgconfigdir}/tss2-esys.pc
%{_pkgconfigdir}/tss2-fapi.pc
%{_pkgconfigdir}/tss2-mu.pc
%{_pkgconfigdir}/tss2-rc.pc
%{_pkgconfigdir}/tss2-sys.pc
%{_pkgconfigdir}/tss2-tcti-cmd.pc
%{_pkgconfigdir}/tss2-tcti-device.pc
%{_pkgconfigdir}/tss2-tcti-mssim.pc
%{_pkgconfigdir}/tss2-tcti-pcap.pc
%{_pkgconfigdir}/tss2-tcti-swtpm.pc
%{_pkgconfigdir}/tss2-tctildr.pc
%{_mandir}/man3/ESYS_*.3*
%{_mandir}/man3/Esys_*.3*
%{_mandir}/man3/FapiTestgroup.3*
%{_mandir}/man3/Fapi_*.3*
%{_mandir}/man3/Tss2_*.3*
%{_mandir}/man7/tss2-tcti-cmd.7*
%{_mandir}/man7/tss2-tcti-device.7*
%{_mandir}/man7/tss2-tcti-mssim.7*
%{_mandir}/man7/tss2-tcti-swtpm.7*
%{_mandir}/man7/tss2-tctildr.7*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtss2-esys.a
%{_libdir}/libtss2-fapi.a
%{_libdir}/libtss2-mu.a
%{_libdir}/libtss2-rc.a
%{_libdir}/libtss2-sys.a
%{_libdir}/libtss2-tcti-cmd.a
%{_libdir}/libtss2-tcti-device.a
%{_libdir}/libtss2-tcti-mssim.a
%{_libdir}/libtss2-tcti-pcap.a
%{_libdir}/libtss2-tcti-swtpm.a
%{_libdir}/libtss2-tctildr.a
