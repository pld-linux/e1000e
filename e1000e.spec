#
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	1
%define		pname	e1000e
Summary:	Intel(R) PRO/1000e driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel® PRO/1000e
Name:		%{pname}%{_alt_kernel}
Version:	3.3.4
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://downloads.sourceforge.net/e1000/%{pname}-%{version}.tar.gz
# Source0-md5:	5c6d010341868f753cf983cbe4467db5
URL:		http://downloads.sourceforge.net/e1000/
BuildRequires:	rpm-build-macros >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters. This driver is
designed to work with the Intel(R) 82571/2/3/4 PCI-E family of gigabit
adapters and 82567 controllers.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel® PRO/1000. Ten sterownik jest
stworzony aby pracować z kartami gigabitowymi rodziny Intel®
82571/2/3/4 PCI-E oraz kontrolerami 82567.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-net-%{pname}\
Summary:	Intel(R) PRO/1000e driver for Linux\
Summary(pl.UTF-8):	Sterownik do karty Intel® PRO/1000e\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-net-%{pname}\
This package contains the Linux driver for the Intel(R) PRO/1000\
family of 10/100/1000 Ethernet network adapters. This driver is\
designed to work with the Intel(R) 82571/2/3/4 PCI-E family of gigabit\
adapters and 82567 controllers.\
\
%description -n kernel%{_alt_kernel}-net-%{pname} -l pl.UTF-8\
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych\
10/100/1000Mbit z rodziny Intel® PRO/1000. Ten sterownik jest\
stworzony aby pracować z kartami gigabitowymi rodziny Intel®\
82571/2/3/4 PCI-E oraz kontrolerami 82567.\
\
%files -n kernel%{_alt_kernel}-net-%{pname}\
%defattr(755,root,root,755)\
%doc e1000e.7 README\
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf\
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*\
\
%post	-n kernel%{_alt_kernel}-net-%{pname}\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-net-%{pname}\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -C src -m %{pname}\
%install_kernel_modules -D installed -m src/%{pname} -d kernel/drivers/net -n %{pname} -s current\
%{nil}

%define install_kernel_pkg()\
install -d $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}\
# blacklist kernel module\
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'\
blacklist e1000e\
alias e1000e e1000e-current\
EOF\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -q -n %{pname}-%{version}

cat > src/Makefile <<'EOF'
obj-m := e1000e.o
e1000e-objs := netdev.o ethtool.o param.o \
82571.o ich8lan.o 80003es2lan.o \
mac.o nvm.o phy.o manage.o kcompat.o ptp.o

EXTRA_CFLAGS=-DDRIVER_E1000E -DCONFIG_E1000E_SEPARATE_TX_HANDLER
EOF
# add -DE1000E_NO_NAPI to disable NAPI

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{expand:%install_kernel_packages}
cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
