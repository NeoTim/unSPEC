%define beanstalkd_user      beanstalkd
%define beanstalkd_group     %{beanstalkd_user}
%define beanstalkd_home      %{_localstatedir}/lib/beanstalkd
%define beanstalkd_binlogdir %{beanstalkd_home}/binlog

%global _hardened_build 1

Name:           beanstalkd
Version:        1.4.6
Release:        8%{?dist}
Summary:        A simple, fast work-queue service

Group:          System Environment/Daemons
License:        GPLv3+
URL:            http://kr.github.com/%{name}/
Source0:        https://github.com/downloads/kr/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.sysconfig

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libevent-devel
BuildRequires:  systemd-units


Requires(pre):    shadow-utils
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

# fixes dprintf source conflict.  This is patch from upstream's git repository.
# A new release has not been made that includes this patch
# https://github.com/kr/beanstalkd/commit/976ec8ba8e70e3b5027f441de529f479c11c8507
Patch0: 0007-Patch-to-rename-beanstalkd-s-dprintf-to-dbgprintf.patch

%description
beanstalkd is a simple, fast work-queue service. Its interface is generic,
but was originally designed for reducing the latency of page views in
high-volume web applications by running most time-consuming tasks
asynchronously.


%prep
%setup -q
%patch0 -p1

if [ ! -e configure ]; then
  sh autogen.sh
fi


%build
%configure --disable-rpath
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install-man1 DESTDIR=$RPM_BUILD_ROOT
make install-exec-am DESTDIR=$RPM_BUILD_ROOT
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -d -m 0755 %{buildroot}%{beanstalkd_home}
%{__install} -d -m 0755 %{buildroot}%{beanstalkd_binlogdir}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group %{beanstalkd_group} >/dev/null || groupadd -r %{beanstalkd_group}
getent passwd %{beanstalkd_user} >/dev/null || \
    useradd -r -g %{beanstalkd_user} -d %{beanstalkd_home} -s /sbin/nologin \
    -c "beanstalkd user" %{beanstalkd_user}
exit 0


%post
# make the binlog dir after installation, this is so SELinux does not complain
# about the init script creating the binlog directory
# Bug 558310
if [ -d %{beanstalkd_home} ]; then
    %{__install} -d %{beanstalkd_binlogdir} -m 0755 \
        -o %{beanstalkd_user} -g %{beanstalkd_user} \
        %{beanstalkd_binlogdir}
fi

if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc README README-DEVELOPERS README-TESTS COPYING doc/protocol.txt
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,%{beanstalkd_user},%{beanstalkd_group}) %dir %{beanstalkd_home}
%ghost %attr(0755,%{beanstalkd_user},%{beanstalkd_group}) %dir %{beanstalkd_binlogdir}


%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.6-6
- Add systemd config Bug #754490
- fix user/group creation to be in line with packaging standards
- fix Source URL

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 27 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.6-4
- fix f15 build issues with patch from upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 05 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.6-1
- update to upstream 1.4.6

* Mon Feb 22 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.3-2
- fix binlogdir location initialization for bug #55831

* Sun Feb 21 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.3-1
- update to upstream 1.4.3
- change default binlogdir in sysconfig file
- cleanup rpmlint warnings

* Sat Oct 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.2-1
- update to upstream 1.4.2

* Sun Oct 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4-0
- update to upstream 1.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3-1
- update to upstream 1.3

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.2-1
- update to upstream 1.2
- remove man page source as it was incorporated upstream

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.1-1
- initial spec creation
