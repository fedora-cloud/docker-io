# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

# docker builds in a checksum of dockerinit into docker,
# so stripping the binaries breaks docker
%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         docker
%global repo            %{project}

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit      a8a31eff10544860d2188dddabdee4d727545796
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:       %{repo}-io
Version:    1.5.0
Release:    1%{?dist}
Summary:    Automates deployment of containerized applications
License:    ASL 2.0
URL:        http://www.docker.com
# only x86_64 for now: https://github.com/docker/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://github.com/docker/docker/archive/v%{version}.tar.gz
# though final name for sysconf file is simply 'docker',
# having .sysconfig makes things clear
Source1:    docker.sysconfig
Source2:    docker-storage.sysconfig
# have init script wait up to 5 mins before forcibly terminating docker daemon
# https://github.com/docker/docker/commit/640d2ef6f54d96ac4fc3f0f745cb1e6a35148607
Source3:    docker.sysvinit
Source4:    docker-network.sysconfig
Source5:    docker-logrotate.sh
Source6:    README.%{repo}-logrotate
BuildRequires:  glibc-static
BuildRequires:  golang >= 1.3.3
# for gorilla/mux and kr/pty https://github.com/dotcloud/docker/pull/5950
#BuildRequires:  golang(github.com/gorilla/mux) >= 0-0.13
#BuildRequires:  golang(github.com/kr/pty) >= 0-0.19
#BuildRequires:  golang(github.com/godbus/dbus)
# for coreos/go-systemd https://github.com/dotcloud/docker/pull/5981
#BuildRequires:  golang(github.com/coreos/go-systemd) >= 2-1
#BuildRequires:  golang(code.google.com/p/go.net/websocket)
#BuildRequires:  golang(code.google.com/p/gosqlite/sqlite3)
# RHBZ#1109039 use syndtr/gocapability >= 0-0.7
#BuildRequires:  golang(github.com/syndtr/gocapability/capability) >= 0-0.7
#BuildRequires:  golang(github.com/docker/libcontainer) >= 1.2.0
#BuildRequires:  golang(github.com/tchap/go-patricia/patricia)
#BuildRequires:  golang(github.com/docker/libtrust)
#BuildRequires:  golang(github.com/docker/libtrust/trustgraph)
BuildRequires:  sqlite-devel
BuildRequires:  go-md2man
BuildRequires:  device-mapper-devel
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(postun):   initscripts
# need xz to work with ubuntu images
# Resolves: rhbz#1045220
Requires:   xz
# Resolves: rhbz#1035436
Requires:   bridge-utils
Requires:   lxc

# Resolves: rhbz#1173950
Requires:   device-mapper-libs

# Resolves: rhbz#1034919
# No longer needed in Fedora because of libcontainer
Requires:   libcgroup

Provides:   lxc-docker = %{version}

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%package devel
BuildRequires:  golang >= 1.2.1-3
Requires:   golang >= 1.2.1-3
Provides:   %{name}-pkg-devel
Summary:    A golang registry for global request variables (source libraries)
Provides: golang(%{import_path}) = %{version}-%{release}
Provides: golang(%{import_path}/builder) = %{version}-%{release}
Provides: golang(%{import_path}/builder/parser) = %{version}-%{release}
Provides: golang(%{import_path}/builder/parser/dumper) = %{version}-%{release}
Provides: golang(%{import_path}/builder/command) = %{version}-%{release}
Provides: golang(%{import_path}/nat) = %{version}-%{release}
Provides: golang(%{import_path}/dockerversion) = %{version}-%{release}
Provides: golang(%{import_path}/utils) = %{version}-%{release}
Provides: golang(%{import_path}/integration-cli) = %{version}-%{release}
Provides: golang(%{import_path}/trust) = %{version}-%{release}
Provides: golang(%{import_path}/events) = %{version}-%{release}
Provides: golang(%{import_path}/volumes) = %{version}-%{release}
Provides: golang(%{import_path}/dockerinit) = %{version}-%{release}
Provides: golang(%{import_path}/engine) = %{version}-%{release}
Provides: golang(%{import_path}/registry) = %{version}-%{release}
Provides: golang(%{import_path}/registry/v2) = %{version}-%{release}
Provides: golang(%{import_path}/api) = %{version}-%{release}
Provides: golang(%{import_path}/api/client) = %{version}-%{release}
Provides: golang(%{import_path}/api/stats) = %{version}-%{release}
Provides: golang(%{import_path}/api/server) = %{version}-%{release}
Provides: golang(%{import_path}/opts) = %{version}-%{release}
Provides: golang(%{import_path}/builtins) = %{version}-%{release}
Provides: golang(%{import_path}/runconfig) = %{version}-%{release}
Provides: golang(%{import_path}/docker) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/docker-device-tool) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/host-integration) = %{version}-%{release}
Provides: golang(%{import_path}/daemon) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/devmapper) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/aufs) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/overlay) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/vfs) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/btrfs) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/graphdriver/graphtest) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/networkdriver) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/networkdriver/ipallocator) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/networkdriver/portmapper) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/networkdriver/bridge) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/networkdriver/portallocator) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/execdriver) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/execdriver/execdrivers) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/execdriver/lxc) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/execdriver/native) = %{version}-%{release}
Provides: golang(%{import_path}/daemon/execdriver/native/template) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/devicemapper) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/units) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/chrootarchive) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mount) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/systemd) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers/kernel) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers/operatingsystem) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/parsers/filters) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/broadcastwriter) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/stdcopy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/promise) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pools) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/system) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fileutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mflag) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mflag/example) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/timeutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ioutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pubsub) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/signal) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/listenbuffer) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/httputils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/urlutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/sysinfo) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/archive) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/iptables) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/tailfile) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/graphdb) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/tarsum) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/namesgenerator) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/jsonlog) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/truncindex) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/homedir) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/symlink) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/networkfs/resolvconf) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/networkfs/etchosts) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/reexec) = %{version}-%{release}
Provides: golang(%{import_path}/integration) = %{version}-%{release}
Provides: golang(%{import_path}/links) = %{version}-%{release}
Provides: golang(%{import_path}/image) = %{version}-%{release}
Provides: golang(%{import_path}/graph) = %{version}-%{release}

%description devel
This is the source libraries for docker.

%package fish-completion
Summary:    fish completion files for docker
Requires:   %{name} = %{version}-%{release}
Provides:   %{repo}-fish-completion = %{version}-%{release}

%description fish-completion
This package installs %{summary}.

%package logrotate
Summary:    cron job to run logrotate on docker containers
Requires:   %{name} = %{version}-%{release}
Provides:   %{repo}-logrotate = %{version}-%{release}

%description logrotate
This package installs %{summary}. logrotate is assumed to be installed on
containers for this to work, failures are silently ignored.

%package vim
Summary:    vim syntax highlighting files for docker
Requires:   %{name} = %{version}-%{release}
Requires:   vim
Provides:   %{repo}-vim = %{version}-%{release}

%description vim
This package installs %{summary}.

%package zsh-completion
Summary:    zsh completion files for docker
Requires:   %{name} = %{version}-%{release}
Requires:   zsh
Provides:   %{repo}-zsh-completion = %{version}-%{release}

%description zsh-completion
This package installs %{summary}.

%prep
%setup -q -n docker-%{version}
cp %{SOURCE6} .

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/docker
ln -s $(pwd) ./_build/src/github.com/docker/docker

export DOCKER_GITCOMMIT="%{shortcommit}/%{version}"
export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}
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
install -dp %{buildroot}%{_datadir}/bash-completion/completions
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions

# install fish completion
# create, install and own /usr/share/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/fish/%{repo}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install container logrotate cron script
install -dp %{buildroot}%{_sysconfdir}/cron.daily/
install -p -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.daily/%{repo}-logrotate

# install zsh completion
# zsh completion has been upstreamed into docker and
# this will be removed once it enters the zsh rpm
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions

# install vim syntax highlighting
# (in the process of being upstreamed into vim)
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
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/docker
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/docker-storage
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/docker-network
install -d %{buildroot}%{_initddir}
install -p -m 755 %{SOURCE3} %{buildroot}%{_initddir}/docker

# sources
install -d -p %{buildroot}/%{gopath}/src/%{import_path}
rm -rf pkg/symlink/testdata

for dir in api builder builtins contrib/docker-device-tool \
        contrib/host-integration daemon docker dockerinit \
        dockerversion engine events graph \
        image links nat opts pkg registry runconfig \
        trust utils volumes
do
    cp -rpav $dir %{buildroot}/%{gopath}/src/%{import_path}/
done

# install docker config directory
install -dp %{buildroot}%{_sysconfdir}/docker/

%check
[ ! -e /run/docker.sock ] || {
    mkdir test_dir
    pushd test_dir
    git clone https://%{import_path}
    pushd docker
    make test
    popd
    popd
}

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
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md 
%doc LICENSE-vim-syntax README-vim-syntax.md
%config(noreplace) %{_sysconfdir}/sysconfig/docker
%config(noreplace) %{_sysconfdir}/sysconfig/docker-storage
%config(noreplace) %{_sysconfdir}/sysconfig/docker-network
%{_mandir}/man1/docker*.1.gz
%{_mandir}/man5/Dockerfile.5.gz
%{_bindir}/docker
%{_libexecdir}/docker
%{_initddir}/docker
%{_datadir}/bash-completion/completions/docker
%dir %{_sharedstatedir}/docker
%{_sysconfdir}/udev/rules.d/80-docker.rules
%{_sysconfdir}/docker

%files devel
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md LICENSE MAINTAINERS NOTICE README.md 
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%dir %{gopath}/src/%{import_path}
%{gopath}/src/%{import_path}/*

%files fish-completion
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/docker.fish

%files logrotate
%doc README.%{repo}-logrotate
%{_sysconfdir}/cron.daily/%{repo}-logrotate

%files vim
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim

%files zsh-completion
%{_datadir}/zsh/site-functions/_docker

%changelog
* Wed Feb 18 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.5.0-1
- Resolves: rhbz#1191438 - update to 1.5.0
- patched sysvinit file via upstream docker PR#10277 to fix stale
pidfile issue when docker dies abruptly, thanks to
Mike Leone <mleone896@gmail.com>
- merge -pkg-devel into -devel subpackage

* Fri Jan 16 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4.1-4
- run tests inside docker repo in check (doesn't affect koji - not built)

* Thu Jan 15 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4.1-3
- set DOCKER_CERT_PATH outside of sysconfig file

* Wed Jan 07 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4.1-2
- don't require fish for fish-completion as it's unavailable

* Mon Jan 05 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4.1-1
- Resolves: rhbz#1175144 - update to 1.4.1
- patch to make 'docker exec' work
via Vincent Batts <vbatts@fedoraproject.org>
https://github.com/docker/libcontainer/issues/309
- subpackages for fish, zsh completion, vim highlighting and logrotate cron
job

* Mon Dec 15 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4.0-2
- Resolves: rhbz#1173950 remove min version requirements on device-mapper-libs

* Thu Dec 11 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4.0-1
- Resolves: rhbz#1173325
- Resolves: rhbz#1172761 - CVE-2014-9356
- Resolves: rhbz#1172782 - CVE-2014-9357
- Resolves: rhbz#1172787 - CVE-2014-9358
- update to upstream v1.4.0
- override DOCKER_CERT_PATH in sysconfig instead of patching the source
- update metaprovides
- define PR_SET_CHILD_SUBREAPER as per newer kernel-headers

* Tue Nov 25 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.2-2
- Resolves: rhbz#1167642 - Update to upstream v1.3.2
- Resolves: rhbz#1167505, rhbz#1167508 - CVE-2014-6407
- Resolves: rhbz#1167506 - CVE-2014-6408
- use vendor dir for golang deps (fix their rpms soon)
- keep NVRs in sync with rest of fedora

* Fri Oct 31 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.1-2
- Remove pandoc from build reqs

* Fri Oct 31 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.1-1
- update to v1.3.1

* Mon Oct 20 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3.0-1
- Resolves: rhbz#1153936 - update to v1.3.0
- iptables=false => ip-masq=false

* Thu Oct 09 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.2.0-3
- Resolves: rhbz#1139415 - correct path for bash completion
    /usr/share/bash-completion/completions
- sysvinit script update as per upstream commit 
    640d2ef6f54d96ac4fc3f0f745cb1e6a35148607 
- don't own dirs for vim highlighting, bash completion and udev

* Thu Sep 25 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.2.0-2
- Resolves: rhbz#1145660 - support /etc/sysconfig/docker-storage 
  From: Colin Walters <walters@redhat.com>
- patch to ignore selinux if it's disabled
  https://github.com/docker/docker/commit/9e2eb0f1cc3c4ef000e139f1d85a20f0e00971e6
  From: Dan Walsh <dwalsh@redhat.com>
- Resolves: rhbz#1139415 - correct path for bash completion
- init script waits upto 5 mins before terminating daemon

* Sat Aug 23 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.2.0-1
- Resolves: rhbz#1132824 - update to v1.2.0

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
