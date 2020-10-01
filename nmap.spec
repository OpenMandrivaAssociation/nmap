%define _disable_ld_no_undefined 1
%define _disable_lto 1
%define _disable_rebuild_configure 1

Summary:	Network exploration tool and security scanner
Name:		nmap
Epoch:		1
Version:	7.80
Release:	3
License:	GPLv2
Group:		Networking/Other
Url:		http://nmap.org/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%{version}.tar.bz2
Source2:	nmap.rpmlintrc
BuildRequires:	pkgconfig(libpcap)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(lua)
%rename	%{name}-ndiff
%rename	%{name}-frontend

%description
Nmap is a utility for network exploration or security auditing. It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, sunRPC scanning, reverse-identd scanning, and
more.

%prep
%autosetup -p1

# (tpg) remove bundled libs
rm -rf libpcap libpcre macosx mswin32 libssh2 libz

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure*

%build
%configure \
	--without-nmap-update \
	--without-zenmap \
	--without-ndiff \
	--with-libpcap=yes \
	--with-liblua=yes \
	--with-libz=yes \
	--with-libpcre=yes \
	--with-libssh2=yes

%make_build

%install
%make_install nmapdatadir=%{_datadir}/nmap STRIP=/bin/true

install -m0644 docs/zenmap.1 %{buildroot}%{_mandir}/man1/

rm -f %{buildroot}%{_datadir}/applications/*.desktop
rm -f %{buildroot}%{_datadir}/ncat/ca-bundle.crt
rmdir %{buildroot}%{_datadir}/ncat
rm -f %{buildroot}%{_bindir}/uninstall_*

%find_lang %{name} --with-man

%files -f %{name}.lang
%doc COPYING* HACKING docs/README docs/nmap.usage.txt
%{_bindir}/%{name}
%{_bindir}/ncat
%{_bindir}/nping
%{_datadir}/%{name}
%{_mandir}/man1/nmap.*
%{_mandir}/man1/ncat.*
%{_mandir}/man1/nping.*
%{_mandir}/man1/zenmap.*
