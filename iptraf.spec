Summary:	A console-based network monitoring program
Name:		iptraf
Version:	3.0.1
Release:	5
Group:		Monitoring
License:	GPLv2+
URL:		https://iptraf.seul.org/
Source0:	ftp://iptraf.seul.org/pub/iptraf/%{name}-%{version}.tar.gz
Source1:	iptraf 
Patch0:		iptraf-2.4.0-Makefile.patch
Patch1:		iptraf-2.7.0-install.patch
Patch2:		iptraf-2.7.0-doc.patch
Patch3:		iptraf-2.7.0-nostrip.patch
Patch4:		iptraf-3.0.0-setlocale.patch
Patch5:		iptraf-3.0.0-longdev.patch
Patch6:		iptraf-3.0.1-compile.fix.patch
Patch7:		iptraf-3.0.0-in_trafic.patch
Patch8:		iptraf-3.0.1-incltypes.patch
Patch9:		iptraf-3.0.0-ifname.patch
Patch10:	iptraf-3.0.0-interface.patch
Patch11:	iptraf-3.0.1-ipv6.patch
Patch12:	iptraf-3.0.1-ipv6-fix.patch
Patch13:	iptraf-3.0.0-strcpy-overlap-memory.patch
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(ncursesw)

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
%patch6 -p1 -b .compile
%patch11 -p1 -b .ipv6
%patch12 -p1 -b .ipv6-fix
%patch0 -p1 -b .Makefile
%patch1 -p1 -b .install
%patch2 -p1 -b .doc
%patch3 -p1 -b .nostrip
%patch4 -p1 -b .setlocale
%patch5 -p1 -b .longdev
%patch7 -p1 -b .in_trafic
%patch8 -p1 -b .incltypes
%patch9 -p0 -b .ifname
%patch10 -p1 -b .interface
%patch13 -p1



%build
find -name "*.c" -o -name "*.h"|while read src; do
	sed -i "s%<linux/if_ether.h>%<netinet/if_ether.h>%" $src
	sed -i "s%<linux/if_tr.h>%<netinet/if_tr.h>%" $src
	sed -i "s%<linux/if_fddi.h>%<netinet/if_fddi.h>%" $src
done

%serverbuild

%make -C src \
    TARGET=%{_prefix}/sbin \
    LOCKDIR=/var/lock/iptraf \
    LOGDIR=/var/log/iptraf \
    WORKDIR=%{_localstatedir}/lib/iptraf

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}/var/log/iptraf
install -d %{buildroot}/var/lock/iptraf
install -d %{buildroot}%{_localstatedir}/lib/iptraf

install -m 755 src/{iptraf,rvnamed} %{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/iptraf

install -d %{buildroot}%{_mandir}/man8
install -m644 Documentation/*.8 %{buildroot}%{_mandir}/man8


# clean up
rm -f Documentation/Makefile
rm -f Documentation/iptraf.xpm
rm -f Documentation/manual.template.gz
rm -f Documentation/version.awk
rm -f Documentation/version
rm -f Documentation/stylesheet-images/.eps

%files
%doc CHANGES INSTALL README* FAQ
%doc Documentation
%dir %attr(644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/iptraf
%{_sbindir}/*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/iptraf
%dir /var/log/iptraf
%dir /var/lock/iptraf
