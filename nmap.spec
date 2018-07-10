%define _disable_ld_no_undefined 1
%define _disable_lto 1
%define _disable_rebuild_configure 1

Summary:	Network exploration tool and security scanner
Name:		nmap
Epoch:		1
Version:	7.50
Release:	2
License:	GPLv2
Group:		Networking/Other
Url:		http://nmap.org/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%{version}.tar.bz2
Source1:	%{name}_icons.tar.bz2
Source2:	nmap.rpmlintrc
BuildRequires:	libpcap-devel
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python2) >= 2.4

%description
Nmap is a utility for network exploration or security auditing. It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, sunRPC scanning, reverse-identd scanning, and
more.

%package	frontend
Summary:	Multi-platform graphical Nmap frontend and results viewer
Group:		Networking/Other
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pygtk2
Requires(post,postun):	desktop-file-utils

%description	frontend
Zenmap is an Nmap frontend. It is meant to be useful for advanced users and to
make Nmap easy to use by beginners. It was originally derived from Umit, an
Nmap GUI created as part of the Google Summer of Code.

%prep
%setup -q -a1

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
export ac_cv_path_PYTHON=%{_bindir}/python2
%configure --without-nmap-update --without-liblua
%make

%install
unset PYTHONDONTWRITEBYTECODE
%makeinstall_std nmapdatadir=%{_datadir}/nmap STRIP=/bin/true

install -m0644 docs/zenmap.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}{%_miconsdir,%_liconsdir}
install -m0644 %{name}16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 %{name}32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 %{name}48.png %{buildroot}%{_liconsdir}/%{name}.png

rm -f %{buildroot}%{_datadir}/applications/*.desktop

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{_vendor}-%{name}.desktop << EOF
[Desktop Entry]
Name=Nmap
Name[ru]=Nmap
Comment=A frontend for the nmap port scanner
Comment[ru]=Интерфейс для сканера портов nmap
Exec=zenmap
Icon=%{name}
Terminal=false
Type=Application
Categories=System;Monitor;
EOF

%find_lang %{name} --with-man

# cleanup
rm -f %{buildroot}%{_bindir}/uninstall_zenmap

# Mark python scripts as executable
find %{buildroot}%{python2_sitelib} -type f -name "*py" -exec sed -i 's+#!/usr/bin/env python++' {} \;

%files -f %{name}.lang
%doc COPYING* HACKING docs/README docs/nmap.usage.txt
%{_bindir}/%{name}
%{_bindir}/ncat
%{_bindir}/ndiff
%{_bindir}/nping
%{_bindir}/uninstall_ndiff
%{_datadir}/%{name}
%{_mandir}/man1/nmap.*
%{_mandir}/man1/ncat.*
%{_mandir}/man1/ndiff.*
%{_mandir}/man1/nping.*
%{_datadir}/ncat

%files frontend
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{_bindir}/zenmap
%{python2_sitelib}/*
%{_datadir}/zenmap
%{_datadir}/applications/*.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_mandir}/man1/zenmap.1*
