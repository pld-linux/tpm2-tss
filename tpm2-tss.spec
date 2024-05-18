#
# Conditional build:
%bcond_with	libftdi1	# build with libftdi1 instead of old libftdi
%bcond_with	mbedtls		# mbedTLS crypto instead of OpenSSL
%bcond_without	static_libs	# static libraries

Summary:	OSS implementation of the TCG TPM2 Software Stack (TSS2)
Summary(pl.UTF-8):	Mająca otwarte źródła implementacja TCG TPM2 Software Stack (TSS2)
Name:		tpm2-tss
Version:	4.1.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/tpm2-software/tpm2-tss/releases
Source0:	https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	aae8af8e88dcd1dfe152e1a3f590ef6f
Patch0:		prefer-libftdi1.patch
URL:		https://github.com/tpm2-software/tpm2-tss
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	json-c-devel >= 0.13
# or libftdi1-devel, but version 0 is preferred (as of tpm2-tss 4.1.1)
%if %{with libftdi1}
BuildRequires:	libftdi1-devel
%else
BuildRequires:	libftdi-devel
%endif
BuildRequires:	libltdl-devel >= 2:2
BuildRequires:	libtool >= 2:2
BuildRequires:	libtpms-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	libuuid-devel
%{?with_mbedtls:BuildRequires:	mbedtls-devel}
%{!?with_mbedtls:BuildRequires:	openssl-devel >= 1.1.0}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	sed >= 4.0
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(tss)
Provides:	user(tss)
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
Requires:	json-c-devel >= 0.13
Requires:	libftdi-devel
Requires:	libusb-devel >= 1.0
Requires:	libuuid-devel
%{?with_mbedtls:Requires:	mbedtls-devel >= 1.6.0}
%{!?with_mbedtls:Requires:	openssl-devel >= 1.1.0}

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
%{?with_libftdi1:%patch0 -p1}

# set VERSION properly when there is no .git directory
%{__sed} -i -e 's/m4_esyscmd_s(\[git describe --tags --always --dirty\])/%{version}/' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	systemd_sysusers=yes \
	systemd_tmpfiles=yes \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
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

# tss user home (shared with trousers)
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/tpm

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 139 tss
%useradd -u 139 -d %{_localstatedir}/lib/tpm -s /bin/false -c "TrouSerS user" -g tss tss

%post   -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove tss
	%groupremove tss
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE MAINTAINERS.md README.md
%attr(755,root,root) %{_libdir}/libtss2-esys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-esys.so.0
%attr(755,root,root) %{_libdir}/libtss2-fapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-fapi.so.1
%attr(755,root,root) %{_libdir}/libtss2-mu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-mu.so.0
%attr(755,root,root) %{_libdir}/libtss2-policy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-policy.so.0
%attr(755,root,root) %{_libdir}/libtss2-rc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-rc.so.0
%attr(755,root,root) %{_libdir}/libtss2-sys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-sys.so.1
%attr(755,root,root) %{_libdir}/libtss2-tcti-cmd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-cmd.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-device.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-device.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-i2c-ftdi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-i2c-ftdi.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-i2c-helper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-i2c-helper.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-libtpms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-libtpms.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-mssim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-mssim.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-pcap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-pcap.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-spi-ftdi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-spi-ftdi.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-spi-helper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-spi-helper.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-spi-ltt2go.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-spi-ltt2go.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-spidev.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-spidev.so.0
%attr(755,root,root) %{_libdir}/libtss2-tcti-swtpm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tcti-swtpm.so.0
%attr(755,root,root) %{_libdir}/libtss2-tctildr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2-tctildr.so.0
%dir %{_sysconfdir}/tpm2-tss
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tpm2-tss/fapi-config.json
%dir %{_sysconfdir}/tpm2-tss/fapi-profiles
%{_sysconfdir}/tpm2-tss/fapi-profiles/P_ECCP256SHA256.json
%{_sysconfdir}/tpm2-tss/fapi-profiles/P_ECCP384SHA384.json
%{_sysconfdir}/tpm2-tss/fapi-profiles/P_RSA2048SHA256.json
%{_sysconfdir}/tpm2-tss/fapi-profiles/P_RSA3072SHA384.json
# tss user home (shared with trousers)
%attr(700,tss,tss) %{_localstatedir}/lib/tpm
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
%attr(755,root,root) %{_libdir}/libtss2-policy.so
%attr(755,root,root) %{_libdir}/libtss2-rc.so
%attr(755,root,root) %{_libdir}/libtss2-sys.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-cmd.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-device.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-i2c-ftdi.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-i2c-helper.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-libtpms.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-mssim.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-pcap.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-spi-ftdi.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-spi-helper.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-spi-ltt2go.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-spidev.so
%attr(755,root,root) %{_libdir}/libtss2-tcti-swtpm.so
%attr(755,root,root) %{_libdir}/libtss2-tctildr.so
%{_includedir}/tss2
%{_pkgconfigdir}/tss2-esys.pc
%{_pkgconfigdir}/tss2-fapi.pc
%{_pkgconfigdir}/tss2-mu.pc
%{_pkgconfigdir}/tss2-policy.pc
%{_pkgconfigdir}/tss2-rc.pc
%{_pkgconfigdir}/tss2-sys.pc
%{_pkgconfigdir}/tss2-tcti-cmd.pc
%{_pkgconfigdir}/tss2-tcti-device.pc
%{_pkgconfigdir}/tss2-tcti-i2c-ftdi.pc
%{_pkgconfigdir}/tss2-tcti-i2c-helper.pc
%{_pkgconfigdir}/tss2-tcti-libtpms.pc
%{_pkgconfigdir}/tss2-tcti-mssim.pc
%{_pkgconfigdir}/tss2-tcti-pcap.pc
%{_pkgconfigdir}/tss2-tcti-spi-ftdi.pc
%{_pkgconfigdir}/tss2-tcti-spi-helper.pc
%{_pkgconfigdir}/tss2-tcti-spi-ltt2go.pc
%{_pkgconfigdir}/tss2-tcti-spidev.pc
%{_pkgconfigdir}/tss2-tcti-swtpm.pc
%{_pkgconfigdir}/tss2-tctildr.pc
%{_mandir}/man3/ESYS_*.3*
%{_mandir}/man3/Esys_*.3*
%{_mandir}/man3/FapiTestgroup.3*
%{_mandir}/man3/Fapi_*.3*
%{_mandir}/man3/Tss2_*.3*
%{_mandir}/man7/tss2-tcti-cmd.7*
%{_mandir}/man7/tss2-tcti-device.7*
%{_mandir}/man7/tss2-tcti-i2c-ftdi.7*
%{_mandir}/man7/tss2-tcti-i2c-helper.7*
%{_mandir}/man7/tss2-tcti-mssim.7*
%{_mandir}/man7/tss2-tcti-spi-ftdi.7*
%{_mandir}/man7/tss2-tcti-spi-helper.7*
%{_mandir}/man7/tss2-tcti-spi-ltt2go.7*
%{_mandir}/man7/tss2-tcti-spidev.7*
%{_mandir}/man7/tss2-tcti-swtpm.7*
%{_mandir}/man7/tss2-tctildr.7*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtss2-esys.a
%{_libdir}/libtss2-fapi.a
%{_libdir}/libtss2-mu.a
%{_libdir}/libtss2-policy.a
%{_libdir}/libtss2-rc.a
%{_libdir}/libtss2-sys.a
%{_libdir}/libtss2-tcti-cmd.a
%{_libdir}/libtss2-tcti-device.a
%{_libdir}/libtss2-tcti-i2c-ftdi.a
%{_libdir}/libtss2-tcti-i2c-helper.a
%{_libdir}/libtss2-tcti-libtpms.a
%{_libdir}/libtss2-tcti-mssim.a
%{_libdir}/libtss2-tcti-pcap.a
%{_libdir}/libtss2-tcti-spi-ftdi.a
%{_libdir}/libtss2-tcti-spi-helper.a
%{_libdir}/libtss2-tcti-spi-ltt2go.a
%{_libdir}/libtss2-tcti-spidev.a
%{_libdir}/libtss2-tcti-swtpm.a
%{_libdir}/libtss2-tctildr.a
%endif
