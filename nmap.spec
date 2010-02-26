Summary:	Network exploration tool and security scanner
Name:		nmap
Version:	5.21
Release:	%mkrel 2
Epoch:		1
License:	GPLv2
Group:		Networking/Other
URL:		http://nmap.org/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%{version}.tar.bz2
Source1:	%{name}_icons.tar.bz2
Patch0:		nmap-5.21-libpcap-filter.diff
Patch1:		nmap-4.00-noreturn.diff
BuildRequires:	libpcre-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel >= 2.4
BuildRequires:	lua-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	pygtk2
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description	frontend
Zenmap is an Nmap frontend. It is meant to be useful for advanced users and to
make Nmap easy to use by beginners. It was originally derived from Umit, an
Nmap GUI created as part of the Google Summer of Code.

%prep
%setup -q -n %{name}-%{version} -a1
%patch0 -p1 -b .libpcap-filter
%patch1 -p0 -b .noreturn

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
# update config.* to recognize amd64-*
%{?__cputoolize: %{__cputoolize} -c nsock/src}

%configure2_5x
%make 

%install
rm -rf %{buildroot}
%makeinstall_std nmapdatadir=%{_datadir}/nmap STRIP=/bin/true

install -m0644 docs/zenmap.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}{%_miconsdir,%_liconsdir}
install -m0644 %{name}16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m0644 %{name}32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 %{name}48.png %{buildroot}%{_liconsdir}/%{name}.png

rm -f %{buildroot}%{_datadir}/applications/*.desktop

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Nmap
Comment=A frontend for the nmap port scanner
Exec=%{_bindir}/zenmap
Icon=%{name}
Terminal=false
Type=Application
Categories=System;Monitor;
EOF

%find_lang %{name}

# cleanup
rm -f %{buildroot}%{_bindir}/uninstall_zenmap

%if %mdkversion < 200900
%post frontend
%update_menus
%endif

%if %mdkversion < 200900
%postun frontend
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING* HACKING docs/README docs/nmap.usage.txt
%{_bindir}/%{name}
%{_bindir}/ncat
%{_bindir}/ndiff
%{_datadir}/%{name}
%{_mandir}/man1/nmap.*
%{_mandir}/man1/ncat.*
%{_mandir}/man1/ndiff.*
%{_datadir}/ncat
%lang(de) %{_mandir}/de/man1/nmap.1*
%lang(de) %{_mandir}/es/man1/nmap.1*
%lang(de) %{_mandir}/fr/man1/nmap.1*
%lang(de) %{_mandir}/hr/man1/nmap.1*
%lang(de) %{_mandir}/hu/man1/nmap.1*
%lang(de) %{_mandir}/it/man1/nmap.1*
%lang(de) %{_mandir}/jp/man1/nmap.1*
%lang(de) %{_mandir}/pl/man1/nmap.1*
%lang(de) %{_mandir}/pt_BR/man1/nmap.1*
%lang(de) %{_mandir}/pt_PT/man1/nmap.1*
%lang(de) %{_mandir}/ro/man1/nmap.1*
%lang(de) %{_mandir}/ru/man1/nmap.1*
%lang(de) %{_mandir}/sk/man1/nmap.1*
%lang(de) %{_mandir}/zh/man1/nmap.1*


%files frontend
%defattr(-,root,root)
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{_bindir}/zenmap
%{python_sitelib}/*
%{_datadir}/zenmap
%{_datadir}/applications/*.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_mandir}/man1/zenmap.1*
