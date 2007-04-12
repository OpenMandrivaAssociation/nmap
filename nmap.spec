%define beta	0

Summary:	Network exploration tool and security scanner
Name:		nmap
Version:	4.20
%if %beta
Release:	%mkrel 0.%beta.1
%define theirversion %{version}%beta
%else
Release:	%mkrel 1
%define theirversion %{version}
%endif
Epoch:		1
License:	GPL
Group:		Networking/Other
URL:		http://www.insecure.org/nmap/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%theirversion.tar.bz2
Source1:	%{name}_icons.tar.bz2
Patch0:		nmap-4.00-libpcap-filter.diff
Patch1:		nmap-4.00-noreturn.diff
Patch2:		nmap-4.00-nostrip.diff
BuildRequires:	gtk2-devel
BuildRequires:	libpcre-devel
BuildRequires:	openssl-devel
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
Summary:	Gtk+ frontend for nmap
Group:		Networking/Other
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description	frontend
This package includes nmapfe, a Gtk+ frontend for nmap. The nmap package must
be installed before installing nmap-frontend.

%prep

%setup -q -a1 -n %{name}-%theirversion
%patch0 -p1
%patch1 -p1
%patch2 -p1

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

%makeinstall nmapdatadir=%{buildroot}%{_datadir}/nmap

mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/nmap-frontend <<EOF
?package(nmap-frontend): \
command="%{_bindir}/nmapfe" \
title="Nmap" \
icon="%{name}.png" \
longtitle="A frontend for the nmap port scanner" \
needs="x11" \
section="System/Monitoring" \
xdg="true"
EOF

mkdir -p %{buildroot}{%_miconsdir,%_liconsdir}
install -m 644 %{name}16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{name}32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 %{name}48.png %{buildroot}%{_liconsdir}/%{name}.png

rm -f %{buildroot}%{_datadir}/applications/*.desktop

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Nmap
Comment="A frontend for the nmap port scanner"
Exec="%{_bindir}/nmapfe"
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

%post frontend
%update_menus
%update_desktop_database

%postun frontend
%clean_menus
%clean_desktop_database

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CHANGELOG COPYING* HACKING docs/README docs/nmap.usage.txt
%{_bindir}/nmap
%{_datadir}/%{name}
%{_mandir}/man1/nmap.*

%files frontend
%defattr(-,root,root)
%{_bindir}/nmapfe
%{_bindir}/xnmap
%{_datadir}/applications/*.desktop
%{_menudir}/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_mandir}/man1/nmapfe*
%{_mandir}/man1/xnmap*



