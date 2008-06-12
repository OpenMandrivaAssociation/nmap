Summary:	Network exploration tool and security scanner
Name:		nmap
Version:	4.60
Release:	%mkrel 1
Epoch:		1
License:	GPL
Group:		Networking/Other
URL:		http://nmap.org/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%{version}.tar.bz2
Source1:	%{name}_icons.tar.bz2
Patch0:		nmap-4.00-libpcap-filter.diff
Patch1:		nmap-4.00-noreturn.diff
Patch2:		nmap-4.00-nostrip.diff
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
Requires:	python-sqlite2
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description	frontend
Zenmap is an Nmap frontend. It is meant to be useful for advanced users and to
make Nmap easy to use by beginners. It was originally derived from Umit, an
Nmap GUI created as part of the Google Summer of Code.

%prep

%setup -q -n %{name}-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
# update config.* to recognize amd64-*
#%{?__cputoolize: %{__cputoolize} -c libpcap-possiblymodified}
#%{?__cputoolize: %{__cputoolize} -c libpcre}
%{?__cputoolize: %{__cputoolize} -c nsock/src}

%configure2_5x

%make 

%install
rm -rf %{buildroot}

%makeinstall_std nmapdatadir=%{_datadir}/nmap

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

%files 
%defattr(-,root,root)
%doc CHANGELOG COPYING* HACKING docs/README docs/nmap.usage.txt
%{_bindir}/%{name}
%dir %{_libdir}/%{name}/nselib-bin
%{_libdir}/%{name}/nselib-bin/*.so
%{_datadir}/%{name}
%{_mandir}/man1/nmap.*

%files frontend
%defattr(-,root,root)
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{_bindir}/zenmap
%{python_sitelib}/*
%{_datadir}/pixmaps/*
%{_datadir}/zenmap
%{_datadir}/applications/*.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/icons/*.ico
%{_mandir}/man1/zenmap.1*
