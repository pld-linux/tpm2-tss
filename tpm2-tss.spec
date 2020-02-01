Summary:	OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:		tpm2-tss
Version:	2.3.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fb7e6d371959a65dc6d129af81739742
URL:		https://github.com/tpm2-software/tpm2-tss
BuildRequires:	doxygen
BuildRequires:	libgcrypt-devel
BuildRequires:	openssl-devel
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implementation of the Trusted Computing Group's (TCG) TPM2 Software
Stack (TSS).

%package devel
Summary:	Header files and develpment documentation for tpm2-tss
Summary(es.UTF-8):	Arquivos de cabeçalho e bibliotecas de desenvolvimento para tpm2-tss
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumetacja do tpm2-tss
Summary(pt_BR.UTF-8):	Bibliotecas e arquivos de inclusão para a tpm2-tss
Summary(ru.UTF-8):	Хедеры и библиотеки програмиста для tpm2-tss
Summary(uk.UTF-8):	Хедери та бібліотеки програміста для tpm2-tss
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Implementation of the Trusted Computing Group's (TCG) TPM2 Software
Stack (TSS). Header files and documentation.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja do tpm2-tss.

%description devel -l pt_BR.UTF-8
Tcpdump imprime os cabeçalhos dos pacotes em uma interface de rede.
Ele é muito prático para resolver problemas na rede e para operações
de segurança.

%description devel -l ru.UTF-8
Хедеры и библиотеки програмиста, необходимые для программирования с
tpm2-tss.

%description devel -l uk.UTF-8
Хедери та бібліотеки програміста, необхідні для програмування з
tpm2-tss.

%package static
Summary:	Static tpm2-tss library
Summary(es.UTF-8):	Biblioteca estática usada no desenvolvimento de aplicativos com tpm2-tss
Summary(pl.UTF-8):	Biblioteka statyczna tpm2-tss
Summary(pt_BR.UTF-8):	Biblioteca estática de desenvolvimento
Summary(ru.UTF-8):	Статическая библиотека tpm2-tss
Summary(uk.UTF-8):	Статична бібліотека tpm2-tss
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Implementation of the Trusted Computing Group's (TCG) TPM2 Software
Stack (TSS).

This package contains the static library used for development.

%description static -l pt_BR.UTF-8
Tcpdump imprime os cabeçalhos dos pacotes em uma interface de rede.
Ele é muito prático para resolver problemas na rede e para operações
de segurança.

%description static -l pl.UTF-8
Biblioteka statyczna tpm2-tss.

%description static -l ru.UTF-8
Статическая библиотека, необходимая для программирования с tpm2-tss.

%description static -l uk.UTF-8
Статична бібліотека, необхідна для програмування з tpm2-tss.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--with-udevrulesdir=/lib/udev/rules.d \
	--with-udevrulesprefix=60-

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS README.md RELEASE.md
%attr(755,root,root) %{_libdir}/libtss2*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libtss2*.so.0
%{_mandir}/man7/tss2-*.7*
/lib/udev/rules.d/60-tpm-udev.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtss2*.so
%{_includedir}/tss2
%{_libdir}/libtss2*.la
%{_pkgconfigdir}/tss2*.pc
%{_mandir}/man3/ESYS*.3*
%{_mandir}/man3/Esys*.3*
%{_mandir}/man3/Tss2*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtss2*.a
