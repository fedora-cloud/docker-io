%global debug_package   %{nil}
%global commit          ca5913ff3ec0648d6ad9887abc6cf986fddee1a2
%global gopath          %{_datadir}/gocode

Name:           docker-io
Version:        0.6.3
Release:        3.devicemapper%{?dist}
Summary:        Automates deployment of containerized applications
License:        ASL 2.0

Patch0:         docker-%{version}-alexl-devmapper.patch
Patch1:         docker-%{version}-remove-dotcloud-tar.patch
Patch2:         docker-%{version}-remove-setfcap-from-template.patch
URL:            http://www.docker.io
Source0:        https://github.com/dotcloud/docker/archive/v%{version}.tar.gz
Source1:        docker.service
BuildRequires:  golang("github.com/gorilla/mux")
BuildRequires:  golang("github.com/kr/pty")
BuildRequires:  golang("code.google.com/p/go.net/websocket")
BuildRequires:  device-mapper-devel
BuildRequires:  python-sphinxcontrib-httpdomain
BuildRequires:  pkgconfig(systemd)
Requires:       systemd-units
Requires:       lxc
Requires:       tar
Provides:       lxc-docker

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%prep
%setup -q -n docker-%{version}
%patch0 -p1 -b docker-%{version}-alexl-devmapper.patch
%patch1 -p1 -b docker-%{version}-remove-dotcloud-tar.patch
%patch2 -p1 -b docker-%{version}-remove-setfcap-from-template.patch

%build
mkdir _build
pushd _build

mkdir -p src/github.com/dotcloud
ln -s $(dirs +1 -l) src/github.com/dotcloud/docker
export GOPATH=$(pwd):%{gopath}
go build -v -a github.com/dotcloud/docker/docker
go build -v -a github.com/dotcloud/docker/docker-init

popd

make -C docs/ man

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -d -m 700 %{buildroot}%{_sharedstatedir}/docker
install -p -m 755 _build/docker %{buildroot}%{_bindir}
install -p -m 755 _build/docker-init %{buildroot}%{_bindir}
install -p -m 644 docs/_build/man/docker.1 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 644 contrib/docker.bash %{buildroot}%{_sysconfdir}/bash_completion.d/

%pre
getent group docker > /dev/null || %{_sbindir}/groupadd -r docker
getent passwd docker > /dev/null || %{_sbindir}/useradd -r -g docker\
           -d %{_localstatedir}/lib/docker -s %{_sbindir}/nologin -c\
           "Docker User" docker
exit 0

%post
%systemd_post docker.service

%preun
%systemd_preun docker.service

%postun
%systemd_postun_with_restart docker.service
    
%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md FIXME LICENSE MAINTAINERS NOTICE README.md 
%{_mandir}/man1/docker.1.gz
%{_bindir}/docker
%{_bindir}/docker-init
%{_unitdir}/docker.service
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%dir %{_sharedstatedir}/docker

%changelog
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
