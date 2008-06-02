Summary:	A console-based network monitoring program
Name:		iptraf
Version:	3.0.0
Release:	%mkrel 6
Group:		Monitoring
License:	GPL
URL:		http://iptraf.seul.org/
Source0:	ftp://iptraf.seul.org/pub/iptraf/%{name}-%{version}.tar.bz2
#patches 0 to 10 are from pardus for IPv6 support
Patch0:		iptraf-3.0.0-atheros.patch
Patch1:		iptraf-3.0.0-build.patch
Patch2:		iptraf-3.0.0-linux-headers.patch
Patch3:		iptraf-3.0.0-bnep.patch
Patch4:		iptraf-3.0.0-Makefile.patch
Patch5:		iptraf-3.0.0-headerfix.patch
Patch6:		iptraf-3.0.0-ipv6.patch
Patch7:		iptraf-3.0.0-ipv6-headerfix.patch
Patch8:		iptraf-3.0.0-ncursesw.patch
Patch9:		iptraf-3.0.0-setlocale.patch
Patch10:	iptraf-3.0.0-ipv6-glibc24.patch
Patch100:	iptraf-2.4.0-Makefile.patch
Patch101:	iptraf-2.7.0-install.patch
Patch102:	iptraf-2.7.0-doc.patch
Patch103:	iptraf-2.7.0-interface.patch
Patch104:	iptraf-2.7.0-nostrip.patch
#Patch105:	iptraf-3.0.0-setlocale.patch
Patch106:	iptraf-3.0.0-longdev.patch
Patch107:	iptraf-3.0.0-compile.fix.patch
Patch108:	iptraf-3.0.0-in_trafic.patch
Patch109:	iptraf-3.0.0-incltypes.patch
Patch110:	iptraf-3.0.0-no_splash.diff
BuildRequires:	ncurses-devel
BuildRequires:	libncursesw-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
IPTraf is a console-based network monitoring program for Linux that
displays information about IP traffic.  It returns such information as:

Current TCP connections UDP, ICMP, OSPF, and other types of IP packets
Packet and byte counts on TCP connections IP, TCP, UDP, ICMP, non-IP,
and other packet and byte counts TCP/UDP counts by ports Interface
activity Flag statuses on TCP packets LAN station statistics

This program can be used to determine the type of traffic on your network,
and what kind of service is the most heavily used on what machines, among
others.

IPTraf works on Ethernet, FDDI, ISDN, PLIP, and SLIP/PPP interfaces.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1
%patch2 -p1
%patch3 -p1
%patch4 -p2
%patch5 -p2
%patch6 -p2
%patch7 -p2
%patch8 -p1
%patch9 -p1
%patch10 -p1
#%patch100 -p1 
%patch101 -p1
%patch102 -p1
#%patch103 -p1
%patch104 -p1
#%patch105 -p1
%patch106 -p1
#%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p0

%build
%serverbuild

%make -C src \
    TARGET=%{_prefix}/sbin \
    LOCKDIR=/var/lock/iptraf \
    LOGDIR=/var/log/iptraf \
    WORKDIR=%{_localstatedir}/lib/iptraf

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}/var/log/iptraf
install -d %{buildroot}/var/lock/iptraf
install -d %{buildroot}%{_localstatedir}/lib/iptraf

install -m 755 src/{iptraf,rvnamed} %{buildroot}%{_sbindir}/

mv Documentation/*.8 src/
install -m 644 src/*.8 %{buildroot}%{_mandir}/man8

# clean up
rm -f Documentation/Makefile
rm -f Documentation/iptraf.xpm
rm -f Documentation/manual.template.gz
rm -f Documentation/version.awk
rm -f Documentation/version
rm -f Documentation/stylesheet-images/.eps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES INSTALL README* FAQ
%doc Documentation
%{_sbindir}/*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/iptraf
%dir /var/log/iptraf
%dir /var/lock/iptraf
