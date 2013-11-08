%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%bcond_without  systemd
%endif

#debuginfo not supported with Go
%global debug_package %{nil}
%global gopath  %{_datadir}/gocode

%global commit      1fe08e004686b25aaf56bc01194629c0b7e658f9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           docker-io
Version:        0.7
Release:        0.13.dm%{?dist}
Summary:        Automates deployment of containerized applications
License:        ASL 2.0

Patch0:         docker-0.7-remove-dotcloud-tar.patch
Patch1:         docker-0.7-el6-docs.patch
URL:            http://www.docker.io
# only x86_64 for now: https://github.com/dotcloud/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://github.com/dotcloud/docker/archive/%{commit}/docker-%{shortcommit}.tar.gz
Source1:        docker.service
# though final name for xinetd file is simply 'docker',
# having .xinetd makes things clear
Source2:        docker.xinetd
BuildRequires:  gcc
BuildRequires:  golang(github.com/gorilla/mux)
BuildRequires:  golang(github.com/kr/pty)
BuildRequires:  golang(code.google.com/p/go.net/websocket)
BuildRequires:  device-mapper-devel
BuildRequires:  python-sphinxcontrib-httpdomain
%if %{with systemd}
BuildRequires:  pkgconfig(systemd)
Requires:       systemd-units
%else
Requires:       xinetd
%endif
Requires:       lxc
Requires:       tar
Provides:       lxc-docker = %{version}

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%prep
%setup -q -n docker-%{commit}
rm -rf vendor
%patch0 -p1 -b docker-0.7-remove-dotcloud-tar.patch
%if 0%{?rhel} >= 6
%patch1 -p1 -b docker-0.7-el6-docs.patch
%endif

%build
mkdir _build
pushd _build

mkdir -p src/github.com/dotcloud
ln -s $(dirs +1 -l) src/github.com/dotcloud/docker
export GOPATH=$(pwd):%{gopath}
# passing version information build flags BZ #1017186
export LDFLAGS="-X main.GITCOMMIT %{shortcommit}/%{release} -X main.VERSION %{version} -w"
go build -v -a -ldflags "$LDFLAGS" github.com/dotcloud/docker/docker
go build -v -a -ldflags "$LDFLAGS" github.com/dotcloud/docker/docker-init

popd

make -C docs/ man

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -d -m 700 %{buildroot}%{_sharedstatedir}/docker
install -p -m 755 _build/docker %{buildroot}%{_bindir}
install -p -m 755 _build/docker-init %{buildroot}%{_bindir}
install -p -m 644 docs/_build/man/docker.1 %{buildroot}%{_mandir}/man1
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_sysconfdir}/bash_completion.d/docker.bash
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions
%if %{with systemd}
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
%else
install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/xinetd.d/docker
%endif

%pre
getent group docker > /dev/null || %{_sbindir}/groupadd -r docker
exit 0

%post
%if %{with systemd}
%systemd_post %{SOURCE1}
%endif

%preun
%if %{with systemd}
%systemd_preun %{SOURCE1}
%else
if [ $1 -eq 0 ]; then
    /sbin/service xinetd condrestart > /dev/null 2>&1
fi
%endif

%postun
%if %{with systemd}
%systemd_postun_with_restart %{SOURCE1}
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md FIXME LICENSE MAINTAINERS NOTICE README.md 
%{_mandir}/man1/docker.1.gz
%{_bindir}/docker
%{_bindir}/docker-init
%if %{with systemd}
%{_unitdir}/docker.service
%else
%config(noreplace) %{_sysconfdir}/xinetd.d/docker
%endif
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%{_datadir}/zsh/site-functions/_docker
%dir %{_sharedstatedir}/docker

%changelog
* Sat Nov 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.13.dm
- docker.service file sets iptables rules to allow container networking, this
    is a stopgap approach, relevant pull request here:
    https://github.com/dotcloud/docker/pull/2527

* Sat Oct 26 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.12.dm
- dm branch
- dockerinit -> docker-init

* Tue Oct 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.11.rc4
- passing version information for docker build BZ #1017186

* Sat Oct 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.10.rc4
- rc version bump
- docker-init -> dockerinit
- zsh completion script installed to /usr/share/zsh/site-functions

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.9.rc3
- lxc-docker version matches package version

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.8.rc3
- double quotes removed from buildrequires as per existing golang rules

* Fri Oct 11 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.7.rc3
- xinetd file renamed to docker.xinetd for clarity

* Thu Oct 10 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.6.rc3
- patched for el6 to use sphinx-1.0-build

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.5.rc3
- rc3 version bump
- exclusivearch x86_64

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.4.rc2
- debuginfo not Go-ready yet, skipped

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.3.rc2
- debuginfo package generated
- buildrequires listed with versions where needed
- conditionals changed to reflect systemd or not
- docker commit value not needed
- versioned provides lxc-docker

* Mon Oct 07 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-2.rc2
- rc branch includes devmapper
- el6 BZ #1015865 fix included

* Sun Oct 06 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-1
- version bump, includes devicemapper
- epel conditionals included
- buildrequires sqlite-devel

* Fri Oct 04 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-4.devicemapper
- docker-io service enables IPv4 and IPv6 forwarding
- docker user not needed
- golang not supported on ppc64, docker-io excluded too

* Thu Oct 03 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-3.devicemapper
- Docker rebuilt with latest kr/pty, first run issue solved

* Fri Sep 27 2013 Marek Goldmann <mgoldman@redhat.com> - 0.6.3-2.devicemapper
- Remove setfcap from lxc.cap.drop to make setxattr() calls working in the
  containers, RHBZ#1012952

* Thu Sep 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.3-1.devicemapper
- version bump
- new version solves docker push issues

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-14.devicemapper
- package requires lxc

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-13.devicemapper
- package requires tar

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-12.devicemapper
- /var/lib/docker installed
- package also provides lxc-docker

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-11.devicemapper
- better looking url

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-10.devicemapper
- release tag changed to denote devicemapper patch

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-9
- device-mapper-devel is a buildrequires for alex's code
- docker.service listed as a separate source file

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-8
- install bash completion
- use -v for go build to show progress

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-7
- build and install separate docker-init

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-4
- update to use new source-only golang lib packages

* Sat Sep 21 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-3
- man page generation from docs/.
- systemd service file created
- dotcloud/tar no longer required

* Fri Sep 20 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-2
- patched with alex larsson's devmapper code

* Wed Sep 18 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-1
- Version bump

* Tue Sep 10 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-2
- buildrequires updated
- package renamed to docker-io
 
* Fri Aug 30 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-1
- Version bump
- Package name change from lxc-docker to docker
- Makefile patched from 0.5.3

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-5
- File permissions settings included

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-4
- Credits in changelog modified as per reference's request

* Tue Aug 27 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-3
- Dependencies listed as rpm packages instead of tars
- Install section added

* Mon Aug 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-2
- Github packaging
- Deps not downloaded at build time courtesy Elan Ruusamäe
- Manpage and other docs installed

* Fri Aug 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-1
- Initial fedora package
- Some credit to Elan Ruusamäe (glen@pld-linux.org)
