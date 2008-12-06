# Module for kernels <2.6.24
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		rel	1
%define		pname	e1000e
Summary:	Intel(R) PRO/1000e driver for Linux
Summary(en.UTF-8):	Intel® PRO/1000e driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel® PRO/1000e
Name:		%{pname}%{_alt_kernel}
Version:	0.5.8.2
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/e1000/%{pname}-%{version}.tar.gz
# Source0-md5:	f911e1d04d9d054e6e43f8cf57590409
URL:		http://dl.sourceforge.net/e1000/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters. This driver is
designed to work with the Intel(R) 82571/2/3/4 PCI-E family of gigabit
adapters and 82567 controllers.

%description -l en.UTF-8
This package contains the Linux driver for the Intel® PRO/1000 family
of 10/100/1000 Ethernet network adapters. This driver is designed to
work with the Intel® 82571/2/3/4 PCI-E family of gigabit adapters and
82567 controllers.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel® PRO/1000. Ten sterownik jest
stworzony aby pracować z kartami gigabitowymi rodziny Intel®
82571/2/3/4 PCI-E oraz kontrolerami 82567.

%package -n kernel%{_alt_kernel}-net-%{pname}
Summary:	Intel(R) PRO/1000e driver for Linux
Summary(en.UTF-8):	Intel® PRO/1000e driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel® PRO/1000e
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-%{pname}
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters. This driver is
designed to work with the Intel(R) 82571/2/3/4 PCI-E family of gigabit
adapters and 82567 controllers.

%description -n kernel%{_alt_kernel}-net-%{pname} -l en.UTF-8
This package contains the Linux driver for the Intel® PRO/1000 family
of 10/100/1000 Ethernet network adapters. This driver is designed to
work with the Intel® 82571/2/3/4 PCI-E family of gigabit adapters and
82567 controllers.

%description -n kernel%{_alt_kernel}-net-%{pname} -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel® PRO/1000. Ten sterownik jest
stworzony aby pracować z kartami gigabitowymi rodziny Intel®
82571/2/3/4 PCI-E oraz kontrolerami 82567.

%prep
%setup -q -n %{pname}-%{version}
cat > src/Makefile <<'EOF'
obj-m := e1000e.o
e1000e-objs := netdev.o ethtool.o param.o kcompat.o e1000_80003es2lan.o \
e1000_82571.o e1000_ich8lan.o e1000_mac.o e1000_manage.o e1000_nvm.o \
e1000_phy.o

EXTRA_CFLAGS=-DDRIVER_E1000E
EOF

%build
%build_kernel_modules -C src -m %{pname}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/%{pname} -d kernel/drivers/net -n %{pname} -s current
# blacklist kernel module
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'
blacklist e1000e
alias e1000e e1000e-current
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{pname}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{pname}
%depmod %{_kernel_ver}

%files	-n kernel%{_alt_kernel}-net-%{pname}
%defattr(644,root,root,755)
%doc e1000e.7 README
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*
