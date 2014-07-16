# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

# docker builds in a checksum of dockerinit into docker,
# so stripping the binaries breaks docker
%global debug_package %{nil}

%global import_path github.com/dotcloud/docker
%global commit      63fe64c471e7d76be96a625350468dfc65c06c31
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           docker-io
Version:        1.0.0
Release:        7%{?dist}
Summary:        Automates deployment of containerized applications
License:        ASL 2.0
Patch1:         upstream-patched-archive-tar.patch
Patch2:         finalize-namespace.patch
URL:            http://www.docker.io
# only x86_64 for now: https://github.com/dotcloud/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://github.com/dotcloud/docker/archive/v%{version}.tar.gz
Source1:        docker.service
Source2:        docker.sysconfig
Source3:        docker.socket
# though final name for sysconf/sysvinit files is simply 'docker',
# having .sysvinit and .sysconfig makes things clear
BuildRequires:  gcc
BuildRequires:  glibc-static
# ensure build uses golang 1.2-7 and above
# http://code.google.com/p/go/source/detail?r=a15f344a9efa35ef168c8feaa92a15a1cdc93db5
BuildRequires:  golang >= 1.2-7
# for gorilla/mux and kr/pty https://github.com/dotcloud/docker/pull/5950
BuildRequires:  golang(github.com/gorilla/mux) >= 0-0.13
BuildRequires:  golang(github.com/kr/pty) >= 0-0.19
BuildRequires:  golang(github.com/godbus/dbus)
# for coreos/go-systemd https://github.com/dotcloud/docker/pull/5981
BuildRequires:  golang(github.com/coreos/go-systemd) >= 2-1
BuildRequires:  golang(code.google.com/p/go.net/websocket)
BuildRequires:  golang(code.google.com/p/gosqlite/sqlite3)
# RHBZ#1109039 use syndtr/gocapability >= 0-0.7
BuildRequires:  golang(github.com/syndtr/gocapability/capability) >= 0-0.7
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pandoc
Requires:       systemd-units
# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz
Provides:       lxc-docker = %{version}
# permitted by https://fedorahosted.org/fpc/ticket/341#comment:7
# In F22, the whole package should be renamed to be just "docker" and
# this changed to "Provides: docker-io".
Provides:       docker

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%package devel
BuildRequires:  golang
Requires:       golang
Summary:        A golang registry for global request variables
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/api) = %{version}-%{release}
Provides:       golang(%{import_path}/api/client) = %{version}-%{release}
Provides:       golang(%{import_path}/api/server) = %{version}-%{release}
Provides:       golang(%{import_path}/archive) = %{version}-%{release}
Provides:       golang(%{import_path}/builtins) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/docker-device-tool) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/host-integration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/execdrivers) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/lxc) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/configuration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/template) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/aufs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/btrfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/devmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/graphtest) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/vfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/bridge) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/ipallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/daemonconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/dockerversion) = %{version}-%{release}
Provides:       golang(%{import_path}/engine) = %{version}-%{release}
Provides:       golang(%{import_path}/graph) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/integration) = %{version}-%{release}
Provides:       golang(%{import_path}/integration-cli) = %{version}-%{release}
Provides:       golang(%{import_path}/links) = %{version}-%{release}
Provides:       golang(%{import_path}/nat) = %{version}-%{release}
Provides:       golang(%{import_path}/opts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/graphdb) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/iptables) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/listenbuffer) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag/example) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mount) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/namesgenerator) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/etchosts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/resolvconf) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/signal) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/symlink) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/sysinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/system) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/systemd) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/tailfile) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/truncindex) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/units) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/user) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/runconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/server) = %{version}-%{release}
Provides:       golang(%{import_path}/sysinit) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/broadcastwriter) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/filters) = %{version}-%{release}

%description devel

This is the source libraries for docker.

%prep
%setup -q -n docker-%{version}
rm -rf vendor
%patch1 -p1 -b upstream-patched-archive-tar
%patch2 -p1 -b finalize-namespace

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/dotcloud
ln -s $(pwd) ./_build/src/github.com/dotcloud/docker

export DOCKER_GITCOMMIT="%{shortcommit}/%{version}"
export DOCKER_BUILDTAGS='selinux'
export GOPATH=$(pwd)/_build:%{gopath}

hack/make.sh dynbinary
contrib/man/md/md2man-all.sh
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bundles/%{version}/dynbinary/docker-%{version} %{buildroot}%{_bindir}/docker
# install dockerinit
install -d %{buildroot}%{_libexecdir}/docker
install -p -m 755 bundles/%{version}/dynbinary/dockerinit-%{version} %{buildroot}%{_libexecdir}/docker/dockerinit
# install manpage
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 contrib/man/man1/docker*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 contrib/man/man5/Dockerfile.5 %{buildroot}%{_mandir}/man5
# install bash completion
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_sysconfdir}/bash_completion.d/docker.bash
# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions
# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax
# install udev rules
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -p -m 755 contrib/udev/80-docker.rules %{buildroot}%{_sysconfdir}/udev/rules.d
# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/docker
# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
#install -p -m 644 contrib/init/systemd/docker.service %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}
# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/docker

# sources
install -d -p %{buildroot}/%{gopath}/src/%{import_path}

for dir in api archive builtins daemon daemonconfig dockerversion engine graph \
           image links nat opts pkg registry runconfig server sysinit utils
do
	cp -pav $dir %{buildroot}/%{gopath}/src/%{import_path}/
done

%pre
getent group docker > /dev/null || %{_sbindir}/groupadd -r docker
exit 0

%post
%systemd_post docker

%preun
%systemd_preun docker

%postun
%systemd_postun_with_restart docker

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md FIXME LICENSE MAINTAINERS NOTICE README.md 
%doc LICENSE-vim-syntax README-vim-syntax.md
%{_mandir}/man1/docker*.1.gz
%{_mandir}/man5/Dockerfile.5.gz
%{_bindir}/docker
%dir %{_libexecdir}/docker
%{_libexecdir}/docker/dockerinit
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%{_sysconfdir}/sysconfig/docker
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/docker.bash
%{_datadir}/zsh/site-functions/_docker
%dir %{_sharedstatedir}/docker
%dir %{_sysconfdir}/udev/rules.d
%{_sysconfdir}/udev/rules.d/80-docker.rules
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

%files devel
%defattr(-,root,root,-)
%dir %{gopath}/src/%{import_path}
%{gopath}/src/%{import_path}/api/MAINTAINERS
%{gopath}/src/%{import_path}/api/README.md
%{gopath}/src/%{import_path}/api/*.go
%{gopath}/src/%{import_path}/api/client/*.go
%{gopath}/src/%{import_path}/api/server/*.go
%{gopath}/src/%{import_path}/archive/MAINTAINERS
%{gopath}/src/%{import_path}/archive/README.md
%{gopath}/src/%{import_path}/archive/*.go
%{gopath}/src/%{import_path}/archive/*.goupstream-patched-archive-tar
%{gopath}/src/%{import_path}/archive/testdata/broken.tar
%{gopath}/src/%{import_path}/builtins/*.go
%{gopath}/src/%{import_path}/daemon/*.go
%{gopath}/src/%{import_path}/daemon/README.md
%{gopath}/src/%{import_path}/daemon/execdriver/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/execdriver/execdrivers/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/lxc/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/native/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/native/configuration/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/native/template/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/aufs/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/btrfs/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/btrfs/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/README.md
%{gopath}/src/%{import_path}/daemon/graphdriver/graphtest/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/vfs/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/bridge/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/ipallocator/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/portallocator/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/portmapper/*.go
%{gopath}/src/%{import_path}/daemonconfig/README.md
%{gopath}/src/%{import_path}/daemonconfig/*.go
%{gopath}/src/%{import_path}/dockerversion/*.go
%{gopath}/src/%{import_path}/engine/MAINTAINERS
%{gopath}/src/%{import_path}/engine/*.go
%{gopath}/src/%{import_path}/engine/rengine/*.go
%{gopath}/src/%{import_path}/engine/spawn/*.go
%{gopath}/src/%{import_path}/engine/spawn/subengine/*.go
%{gopath}/src/%{import_path}/graph/*.go
%{gopath}/src/%{import_path}/graph/*.goupstream-patched-archive-tar
%{gopath}/src/%{import_path}/image/*.go
%{gopath}/src/%{import_path}/links/*.go
%{gopath}/src/%{import_path}/nat/*.go
%{gopath}/src/%{import_path}/opts/*.go
%{gopath}/src/%{import_path}/pkg/README.md
%{gopath}/src/%{import_path}/pkg/apparmor/*.go
%{gopath}/src/%{import_path}/pkg/beam/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/beam/*.go
%{gopath}/src/%{import_path}/pkg/beam/data/*.go
%{gopath}/src/%{import_path}/pkg/beam/data/netstring.txt
%{gopath}/src/%{import_path}/pkg/beam/examples/beamsh/beamsh
%{gopath}/src/%{import_path}/pkg/beam/examples/beamsh/*.go
%{gopath}/src/%{import_path}/pkg/beam/examples/beamsh/scripts/*.ds
%{gopath}/src/%{import_path}/pkg/dockerscript/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/dockerscript/*.go
%{gopath}/src/%{import_path}/pkg/dockerscript/scanner/*.go
%{gopath}/src/%{import_path}/pkg/graphdb/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/graphdb/*.go
%{gopath}/src/%{import_path}/pkg/iptables/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/iptables/*.go
%{gopath}/src/%{import_path}/pkg/label/*.go
%{gopath}/src/%{import_path}/pkg/listenbuffer/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/libcontainer/README.md
%{gopath}/src/%{import_path}/pkg/libcontainer/TODO.md
%{gopath}/src/%{import_path}/pkg/libcontainer/cgroups/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/cgroups/fs/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/cgroups/systemd/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/console/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/container.json
%{gopath}/src/%{import_path}/pkg/libcontainer/devices/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/mount/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/mount/nodes/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/namespaces/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/namespaces/init.gofinalize-namespace
%{gopath}/src/%{import_path}/pkg/libcontainer/network/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/nsinit/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/security/capabilities/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/security/restrict/*.go
%{gopath}/src/%{import_path}/pkg/libcontainer/utils/*.go
%{gopath}/src/%{import_path}/pkg/mflag/LICENSE
%{gopath}/src/%{import_path}/pkg/mflag/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/mflag/README.md
%{gopath}/src/%{import_path}/pkg/mflag/example/example.go
%{gopath}/src/%{import_path}/pkg/mflag/*.go
%{gopath}/src/%{import_path}/pkg/mount/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/mount/*.go
%{gopath}/src/%{import_path}/pkg/namesgenerator/*.go
%{gopath}/src/%{import_path}/pkg/netlink/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/netlink/*.go
%{gopath}/src/%{import_path}/pkg/networkfs/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/networkfs/etchosts/*.go
%{gopath}/src/%{import_path}/pkg/networkfs/resolvconf/*.go
%{gopath}/src/%{import_path}/pkg/proxy/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/proxy/*.go
%{gopath}/src/%{import_path}/pkg/selinux/*.go
%{gopath}/src/%{import_path}/pkg/signal/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/signal/*.go
%{gopath}/src/%{import_path}/pkg/symlink/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/symlink/*.go
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/d
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/e
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/f
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/b/h
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/g
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/i
%{gopath}/src/%{import_path}/pkg/sysinfo/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/sysinfo/*.go
%{gopath}/src/%{import_path}/pkg/system/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/system/*.go
%{gopath}/src/%{import_path}/pkg/systemd/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/systemd/*.go
%{gopath}/src/%{import_path}/pkg/term/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/term/*.go
%{gopath}/src/%{import_path}/pkg/testutils/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/testutils/README.md
%{gopath}/src/%{import_path}/pkg/testutils/testutils.go
%{gopath}/src/%{import_path}/pkg/units/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/units/*.go
%{gopath}/src/%{import_path}/pkg/user/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/user/*.go
%{gopath}/src/%{import_path}/pkg/version/*.go
%{gopath}/src/%{import_path}/registry/MAINTAINERS
%{gopath}/src/%{import_path}/registry/*.go
%{gopath}/src/%{import_path}/runconfig/*.go
%{gopath}/src/%{import_path}/server/MAINTAINERS
%{gopath}/src/%{import_path}/server/*.go
%{gopath}/src/%{import_path}/sysinit/README.md
%{gopath}/src/%{import_path}/sysinit/*.go
%{gopath}/src/%{import_path}/utils/filters/*.go
%{gopath}/src/%{import_path}/utils/*.goupstream-patched-archive-tar
%{gopath}/src/%{import_path}/utils/*.go
%{gopath}/src/%{import_path}/utils/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457/json
%{gopath}/src/%{import_path}/utils/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457/layer.tar
%{gopath}/src/%{import_path}/utils/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json
%{gopath}/src/%{import_path}/utils/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/layer.tar

%changelog
* Wed Jul 16 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.0.0-7
- clean up gopath
- add Provides for docker libraries
- produce a -devel with docker source libraries
- accomodate golang rpm macros

* Tue Jul 01 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-6
- Resolves: rhbz#1114810 - CVE-2014-3499 (correct bz#)

* Tue Jul 01 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-5
- Resolves: rhbz#11114810 - CVE-2014-3499

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-4
- Set mode,user,group in docker.socket file

* Sat Jun 14 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-3
- correct bogus date

* Sat Jun 14 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-2
- RHBZ#1109533 patch libcontainer for finalize namespace error
- RHBZ#1109039 build with updated golang-github-syndtr-gocapability
- install Dockerfile.5 manpage

* Mon Jun 09 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1
- upstream version bump to v1.0.0

* Mon Jun 09 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.12.0-1
- RHBZ#1105789 Upstream bump to 0.12.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-11
- unitfile should Require socket file (revert change in release 10)

* Fri May 30 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-10
- do not require docker.socket in unitfile

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-9
- BZ: change systemd service type to 'notify'

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-8
- use systemd socket-activation version

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-7
- add "Provides: docker" as per FPC exception (Matthew Miller
        <mattdm@fedoraproject.org>)

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-6
- don't use docker.sysconfig meant for sysvinit (just to avoid confusion)

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-5
- Bug 1084232 - add /etc/sysconfig/docker for additional args

* Tue May 27 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-4
- patches for BZ 1088125, 1096375

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-3
- add selinux buildtag
- enable selinux in unitfile

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-2
- get rid of conditionals, separate out spec for each branch

* Thu May 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-1
- Bug 1095616 - upstream bump to 0.11.1
- manpages via pandoc

* Mon Apr 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-2
- regenerate btrfs removal patch
- update commit value

* Mon Apr 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-1
- include manpages from contrib

* Wed Apr 09 2014 Bobby Powers <bobbypowers@gmail.com> - 0.10.0-1
- Upstream version bump

* Thu Mar 27 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-1
- BZ 1080799 - upstream version bump

* Thu Mar 13 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.9.0-3
- Add lxc requirement for EPEL6 and patch init script to use lxc driver
- Remove tar dep, no longer needed
- Require libcgroup only for EPEL6

* Tue Mar 11 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-2
- lxc removed (optional)
  http://blog.docker.io/2014/03/docker-0-9-introducing-execution-drivers-and-libcontainer/

* Tue Mar 11 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-1
- BZ 1074880 - upstream version bump to v0.9.0

* Wed Feb 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-1
- Bug 1066841 - upstream version bump to v0.8.1
- use sysvinit files from upstream contrib
- BR golang >= 1.2-7

* Thu Feb 13 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.8.0-3
- Remove unneeded sysctl settings in initscript
  https://github.com/dotcloud/docker/pull/4125

* Sat Feb 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-2
- ignore btrfs for rhel7 and clones for now
- include vim syntax highlighting from contrib/syntax/vim

* Wed Feb 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-1
- upstream version bump
- don't use btrfs for rhel6 and clones (yet)

* Mon Jan 20 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-2
- bridge-utils only for rhel < 7
- discard freespace when image is removed

* Thu Jan 16 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-1
- upstream version bump v0.7.6
- built with golang >= 1.2

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.5-1
- upstream version bump to 0.7.5

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.4-1
- upstream version bump to 0.7.4 (BZ #1049793)
- udev rules file from upstream contrib
- unit file firewalld not used, description changes

* Mon Jan 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-3
- udev rules typo fixed (BZ 1048775)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-2
- missed commit value in release 1, updated now
- upstream release monitoring (BZ 1048441)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-1
- upstream release bump to v0.7.3

* Thu Dec 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-2
- require xz to work with ubuntu images (BZ #1045220)

* Wed Dec 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-1
- upstream release bump to v0.7.2

* Fri Dec 06 2013 Vincent Batts <vbatts@redhat.com> - 0.7.1-1
- upstream release of v0.7.1

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-14
- sysvinit patch corrected (epel only)
- 80-docker.rules unified for udisks1 and udisks2

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-13
- removed firewall-cmd --add-masquerade

* Sat Nov 30 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-12
- systemd for fedora >= 18
- firewalld in unit file changed from Requires to Wants
- firewall-cmd --add-masquerade after docker daemon start in unit file
  (Michal Fojtik <mfojtik@redhat.com>), continue if not present (Michael Young
  <m.a.young@durham.ac.uk>)
- 80-docker.rules included for epel too, ENV variables need to be changed for
  udisks1

* Fri Nov 29 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-11
- Redirect docker log to /var/log/docker (epel only)
- Removed the '-b none' parameter from sysconfig, it's unnecessary since
  we create the bridge now automatically (epel only)
- Make sure we have the cgconfig service started before we start docker,
    RHBZ#1034919 (epel only)

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-10
- udev rules added for fedora >= 19 BZ 1034095
- epel testing pending

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-9
- requires and started after firewalld

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-8
- iptables-fix patch corrected

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-7
- use upstream tarball and patch with mgoldman's commit

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-6
- using mgoldman's shortcommit value 0ff9bc1 for package (BZ #1033606)
- https://github.com/dotcloud/docker/pull/2907

* Wed Nov 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7.0-5
- Fix up EL6 preun/postun to not fail on postun scripts

* Wed Nov 27 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-4
- brctl patch for rhel <= 7

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-3
- Patch how the bridge network is set up on RHEL (BZ #1035436)

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-2
- add libcgroup require (BZ #1034919)

* Tue Nov 26 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-1
- Upstream release 0.7.0
- Using upstream script to build the binary

* Mon Nov 25 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.20.rc7
- correct the build time defines (bz#1026545). Thanks dan-fedora.

* Fri Nov 22 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7-0.19.rc7
- Remove xinetd entry, added sysvinit

* Fri Nov 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.18.rc7
- rc version bump

* Wed Nov 20 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.17.rc6
- removed ExecStartPost lines from docker.service (BZ #1026045)
- dockerinit listed in files

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.16.rc6
- adding back the none bridge patch

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.15.rc6
- update docker source to crosbymichael/0.7.0-rc6
- bridge-patch is not needed on this branch

* Tue Nov 19 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.14.rc5
- update docker source to crosbymichael/0.7-rc5
- update docker source to 457375ea370a2da0df301d35b1aaa8f5964dabfe
- static magic
- place dockerinit in a libexec
- add sqlite dependency

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
