# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

# docker builds in a checksum of dockerinit into docker,
# so stripping the binaries breaks docker
%global debug_package %{nil}

%global import_path github.com/docker/docker
%global commit      d84a070e476ce923dd03e28232564a87704613ab
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           docker-io
Version:        1.1.2
Release:        1%{?dist}
Summary:        Automates deployment of containerized applications
License:        ASL 2.0
Patch1:         upstream-patched-archive-tar.patch
# Resolves: rhbz#1119849 - add AUDIT_WRITE capablility
Patch2:         audit-write.patch
URL:            http://www.docker.com
# only x86_64 for now: https://github.com/docker/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://github.com/docker/docker/archive/v%{version}.tar.gz
# though final name for sysconf file is simply 'docker',
# having .sysconfig makes things clear
Source1:        docker.sysconfig
BuildRequires:  gcc
BuildRequires:  glibc-static
BuildRequires:  pandoc
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
#BuildRequires:  golang(github.com/docker/libcontainer)
BuildRequires:  golang(github.com/tchap/go-patricia/patricia)
BuildRequires:  device-mapper-devel
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(postun):   initscripts
# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1035436
# this won't be needed for rhel7+
Requires:       bridge-utils
Requires:       lxc

# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:       libcgroup

Provides:       lxc-docker = %{version}

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
Requires:       docker-io-pkg-devel
Summary:        A golang registry for global request variables (source libraries)
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
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/runconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/server) = %{version}-%{release}
Provides:       golang(%{import_path}/sysinit) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/broadcastwriter) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/filters) = %{version}-%{release}

%description devel
This is the source libraries for docker.

%package pkg-devel
BuildRequires:  golang
Requires:       golang
Summary:        A golang registry for global request variables (source libraries)
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

%description pkg-devel
These source librariees are provided by docker, but are independent of docker specific logic.
The import paths of %{import_path}/pkg/...

%prep
%setup -q -n docker-%{version}
#rm -rf vendor
%patch1 -p1 -F 2 -b upstream-patched-archive-tar
%patch2 -p1 -F 2
cp -p %{SOURCE1} contrib/init/sysvinit-redhat/docker.sysconfig
rm daemon/execdriver/native/template/*.go.orig

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/dotcloud
ln -s $(pwd) ./_build/src/github.com/dotcloud/docker

export DOCKER_GITCOMMIT="%{shortcommit}/%{version}"
#export DOCKER_BUILDTAGS='selinux'
export GOPATH=$(pwd)/_build:$(pwd)/vendor
export DOCKER_BUILDTAGS='exclude_graphdriver_btrfs'

hack/make.sh dynbinary
docs/man/md2man-all.sh
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
install -p -m 644 docs/man/man1/docker*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 docs/man/man5/Dockerfile.5 %{buildroot}%{_mandir}/man5
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
# install init scripts
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 contrib/init/sysvinit-redhat/docker.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/docker
install -d %{buildroot}%{_initddir}
install -p -m 755 contrib/init/sysvinit-redhat/docker %{buildroot}%{_initddir}/docker

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
# Only do this on install, don't need to re-add each update
if [ $1 -eq 1 ] ; then
  # install but don't activate
  /sbin/chkconfig --add docker
fi

%preun
# Only perform these tasks when erasing, not during updates
if [ $1 -eq 0 ] ; then
  /sbin/service docker stop >/dev/null 2>&1
  /sbin/chkconfig --del docker
fi

%postun
# Needed only during upgrades
if [ $1 -ge 1 ] ; then
  /sbin/service docker condrestart >/dev/null 2>&1 || :
fi

%posttrans
# This is a dirty hack to clean up old-%preun
# Needed only during upgrades

# Previous releases caused an issue with upgrades and chkconfig. 
# Need to clean it up.
if ! /sbin/chkconfig --list docker >/dev/null 2>&1 ; then
  /sbin/chkconfig --add docker 
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md FIXME LICENSE MAINTAINERS NOTICE README.md 
%doc LICENSE-vim-syntax README-vim-syntax.md
%{_mandir}/man1/docker*.1.gz
%{_mandir}/man5/Dockerfile.5.gz
%{_bindir}/docker
%dir %{_libexecdir}/docker
%{_libexecdir}/docker/dockerinit
%config(noreplace) %{_sysconfdir}/sysconfig/docker
%{_initddir}/docker
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
%dir %{gopath}/src/%{import_path}/api
%{gopath}/src/%{import_path}/api/MAINTAINERS
%{gopath}/src/%{import_path}/api/README.md
%{gopath}/src/%{import_path}/api/*.go
%{gopath}/src/%{import_path}/api/client/*.go
%dir %{gopath}/src/%{import_path}/api/server
%{gopath}/src/%{import_path}/api/server/MAINTAINERS
%{gopath}/src/%{import_path}/api/server/*.go
%dir %{gopath}/src/%{import_path}/archive
%{gopath}/src/%{import_path}/archive/MAINTAINERS
%{gopath}/src/%{import_path}/archive/README.md
%{gopath}/src/%{import_path}/archive/*.go
%{gopath}/src/%{import_path}/archive/*.goupstream-patched-archive-tar
%dir %{gopath}/src/%{import_path}/archive/testdata
%{gopath}/src/%{import_path}/archive/testdata/broken.tar
%dir %{gopath}/src/%{import_path}/builtins
%{gopath}/src/%{import_path}/builtins/*.go
%dir %{gopath}/src/%{import_path}/daemon
%{gopath}/src/%{import_path}/daemon/*.go
%{gopath}/src/%{import_path}/daemon/README.md
%dir %{gopath}/src/%{import_path}/daemon/execdriver
%{gopath}/src/%{import_path}/daemon/execdriver/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/MAINTAINERS
%dir %{gopath}/src/%{import_path}/daemon/execdriver/execdrivers
%{gopath}/src/%{import_path}/daemon/execdriver/execdrivers/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/lxc
%{gopath}/src/%{import_path}/daemon/execdriver/lxc/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/execdriver/lxc/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/native
%{gopath}/src/%{import_path}/daemon/execdriver/native/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/native/configuration
%{gopath}/src/%{import_path}/daemon/execdriver/native/configuration/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/native/template
%{gopath}/src/%{import_path}/daemon/execdriver/native/template/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver
%{gopath}/src/%{import_path}/daemon/graphdriver/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/aufs
%{gopath}/src/%{import_path}/daemon/graphdriver/aufs/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/btrfs
%{gopath}/src/%{import_path}/daemon/graphdriver/btrfs/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/btrfs/MAINTAINERS
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/devmapper
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/README.md
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/graphtest
%{gopath}/src/%{import_path}/daemon/graphdriver/graphtest/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/vfs
%{gopath}/src/%{import_path}/daemon/graphdriver/vfs/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/bridge
%{gopath}/src/%{import_path}/daemon/networkdriver/bridge/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/ipallocator
%{gopath}/src/%{import_path}/daemon/networkdriver/ipallocator/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/portallocator
%{gopath}/src/%{import_path}/daemon/networkdriver/portallocator/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/portmapper
%{gopath}/src/%{import_path}/daemon/networkdriver/portmapper/*.go
%dir %{gopath}/src/%{import_path}/daemonconfig
%{gopath}/src/%{import_path}/daemonconfig/README.md
%{gopath}/src/%{import_path}/daemonconfig/*.go
%dir %{gopath}/src/%{import_path}/dockerversion
%{gopath}/src/%{import_path}/dockerversion/*.go
%dir %{gopath}/src/%{import_path}/engine
%{gopath}/src/%{import_path}/engine/MAINTAINERS
%{gopath}/src/%{import_path}/engine/*.go
%dir %{gopath}/src/%{import_path}/graph
%{gopath}/src/%{import_path}/graph/*.go
%{gopath}/src/%{import_path}/graph/*.goupstream-patched-archive-tar
%dir %{gopath}/src/%{import_path}/image
%{gopath}/src/%{import_path}/image/*.go
%dir %{gopath}/src/%{import_path}/links
%{gopath}/src/%{import_path}/links/*.go
%dir %{gopath}/src/%{import_path}/nat
%{gopath}/src/%{import_path}/nat/*.go
%dir %{gopath}/src/%{import_path}/opts
%{gopath}/src/%{import_path}/opts/*.go
%dir %{gopath}/src/%{import_path}/registry
%{gopath}/src/%{import_path}/registry/MAINTAINERS
%{gopath}/src/%{import_path}/registry/*.go
%dir %{gopath}/src/%{import_path}/runconfig
%{gopath}/src/%{import_path}/runconfig/*.go
%dir %{gopath}/src/%{import_path}/server
%{gopath}/src/%{import_path}/server/MAINTAINERS
%{gopath}/src/%{import_path}/server/*.go
%dir %{gopath}/src/%{import_path}/sysinit
%{gopath}/src/%{import_path}/sysinit/README.md
%{gopath}/src/%{import_path}/sysinit/*.go
%dir %{gopath}/src/%{import_path}/utils
%dir %{gopath}/src/%{import_path}/utils/filters
%{gopath}/src/%{import_path}/utils/filters/*.go
%{gopath}/src/%{import_path}/utils/*.goupstream-patched-archive-tar
%{gopath}/src/%{import_path}/utils/*.go
%dir %{gopath}/src/%{import_path}/utils/testdata
%dir %{gopath}/src/%{import_path}/utils/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457
%{gopath}/src/%{import_path}/utils/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457/json
%{gopath}/src/%{import_path}/utils/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457/layer.tar
%dir %{gopath}/src/%{import_path}/utils/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158
%{gopath}/src/%{import_path}/utils/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json
%{gopath}/src/%{import_path}/utils/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/layer.tar

%files pkg-devel
%defattr(-,root,root,-)
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path}/pkg
%{gopath}/src/%{import_path}/pkg/README.md
%dir %{gopath}/src/%{import_path}/pkg/graphdb
%{gopath}/src/%{import_path}/pkg/graphdb/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/graphdb/*.go
%dir %{gopath}/src/%{import_path}/pkg/iptables
%{gopath}/src/%{import_path}/pkg/iptables/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/iptables/*.go
%dir %{gopath}/src/%{import_path}/pkg/listenbuffer
%{gopath}/src/%{import_path}/pkg/listenbuffer/*.go
%dir %{gopath}/src/%{import_path}/pkg/mflag
%{gopath}/src/%{import_path}/pkg/mflag/LICENSE
%{gopath}/src/%{import_path}/pkg/mflag/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/mflag/README.md
%dir %{gopath}/src/%{import_path}/pkg/mflag/example
%{gopath}/src/%{import_path}/pkg/mflag/example/example.go
%{gopath}/src/%{import_path}/pkg/mflag/*.go
%dir %{gopath}/src/%{import_path}/pkg/mount
%{gopath}/src/%{import_path}/pkg/mount/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/mount/*.go
%dir %{gopath}/src/%{import_path}/pkg/namesgenerator
%{gopath}/src/%{import_path}/pkg/namesgenerator/*.go
%dir %{gopath}/src/%{import_path}/pkg/networkfs
%{gopath}/src/%{import_path}/pkg/networkfs/MAINTAINERS
%dir %{gopath}/src/%{import_path}/pkg/networkfs/etchosts
%{gopath}/src/%{import_path}/pkg/networkfs/etchosts/*.go
%dir %{gopath}/src/%{import_path}/pkg/networkfs/resolvconf
%{gopath}/src/%{import_path}/pkg/networkfs/resolvconf/*.go
%dir %{gopath}/src/%{import_path}/pkg/proxy
%{gopath}/src/%{import_path}/pkg/proxy/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/proxy/*.go
%dir %{gopath}/src/%{import_path}/pkg/signal
%{gopath}/src/%{import_path}/pkg/signal/*.go
%dir %{gopath}/src/%{import_path}/pkg/symlink
%{gopath}/src/%{import_path}/pkg/symlink/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/symlink/*.go
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata/fs
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/d
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/e
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/f
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/b
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/b/h
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/g
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/i
%dir %{gopath}/src/%{import_path}/pkg/sysinfo
%{gopath}/src/%{import_path}/pkg/sysinfo/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/sysinfo/*.go
%dir %{gopath}/src/%{import_path}/pkg/system
%{gopath}/src/%{import_path}/pkg/system/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/system/*.go
%dir %{gopath}/src/%{import_path}/pkg/systemd
%{gopath}/src/%{import_path}/pkg/systemd/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/systemd/*.go
%dir %{gopath}/src/%{import_path}/pkg/tailfile
%{gopath}/src/%{import_path}/pkg/tailfile/*.go
%dir %{gopath}/src/%{import_path}/pkg/truncindex
%{gopath}/src/%{import_path}/pkg/truncindex/*.go
%dir %{gopath}/src/%{import_path}/pkg/term
%{gopath}/src/%{import_path}/pkg/term/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/term/*.go
%dir %{gopath}/src/%{import_path}/pkg/testutils
%{gopath}/src/%{import_path}/pkg/testutils/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/testutils/README.md
%{gopath}/src/%{import_path}/pkg/testutils/testutils.go
%dir %{gopath}/src/%{import_path}/pkg/units
%{gopath}/src/%{import_path}/pkg/units/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/units/*.go
%dir %{gopath}/src/%{import_path}/pkg/user
%{gopath}/src/%{import_path}/pkg/user/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/user/*.go
%dir %{gopath}/src/%{import_path}/pkg/version
%{gopath}/src/%{import_path}/pkg/version/*.go

%changelog
* Fri Aug 01 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.1.2-1
- Resolves: rhbz#1124036 - update to upstream v1.1.2

* Thu Jul 31 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-7
- create -devel and -pkg-devel subpackages

* Mon Jul 28 2014 Vincent Batts <vbatts@fedoraproject.org> - 1.0.0-10
- split out the %{import_path}/pkg/... libraries, to avoid cyclic deps with libcontainer

* Thu Jul 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-9
- /etc/sysconfig/docker should be config(noreplace)

* Thu Jun 19 2014 Adam Miller <maxamillion@fedoraproject.org> - 1.0.0-6
- Clean up after ourselves from previous releases. We caused a failure in 
  yum update transactions by removing chkconfig entries.

* Thu Jun 19 2014 Adam Miller <maxamillion@fedoraproject.org> - 1.0.0-5
- Fix up post, preun, postun to handle tasks conditionally based on 
  update vs install vs erase

* Wed Jun 18 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-4
- disable selinux for el6

* Sat Jun 14 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-3
- correct bogus date

* Sat Jun 14 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-2
- RHBZ#1109533 patch libcontainer for finalize namespace error
- RHBZ#1109039 build with updated golang-github-syndtr-gocapability
- install Dockerfile.5 manpage

* Sat Jun 14 2014 Hushan Jia <hushan@zelin.io> - 1.0.0-2
- fix for build on epel6

* Tue Jun 10 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1
- upstream version bump to v1.0.0

* Fri May 30 2014 Vincent Batts <vbatts@redhat.com> - 0.11.1-5
- switch back to the native execdriver, not lxc. bz1103323

* Wed May 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-4
- el6 capabilities fix from Vincent Batts <vbatts@redhat.com>
 https://github.com/vbatts/docker/commit/a8b720e191e149cb9abf4230c0c5fd410282400d

* Tue May 13 2014 Stephen Price <steeef@gmail.com> - 0.11.1-3
- add selinux to sysconfig

* Tue May 13 2014 Stephen Price <steeef@gmail.com> - 0.11.1-2
- add lxc patch back
- use md2man-all.sh to generate man pages
- add selinux

* Mon May 12 2014 Stephen Price <steeef@gmail.com> - 0.11.1-1
- Upstream version bump
- Update changed paths
- Remove lxc patch

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-3
- remove fedora/rhel conditionals (not built)

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
