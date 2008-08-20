%define kname   kernel-uml
%define	name	%{kname}

%define	kversion	2.6.26
%define patchversion 3
%define rel %mkrel 1

%define mdvk %{rel}
%define kernelversionappend -uml.%{mdvk}
%define rpmversion %{kversion}%{?patchversion:.%{patchversion}}
%define mdvkversion %{kversion}%{?patchversion:.%{patchversion}}.%{mdvk}
%define	release	%rel

%define	Summary	The user mode linux kernel

%define bmodulesv %{?!_without_modules:1}%{?_without_modules:0}

Summary:	%{Summary}
Name:		%{name}
Version:	%{rpmversion}
Release:	%{release}
Group:		System/Kernel and hardware

Source0:	linux-%{kversion}.tar.bz2
Source1:    %{name}-config
Source50:   README.mdv
%if %{?patchversion:1}%{?!patchversion:0}
Patch0:     patch-%{kversion}.%{patchversion}.bz2
%endif
License:	GPL
Url:		http://user-mode-linux.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	glibc-static-devel
BuildRequires:  pcap-devel
Requires:       %{kname}-%{_target_cpu} = %{version}-%{release}

%description
User-Mode Linux is a safe, secure way of running Linux versions and
Linux processes. Run buggy software, experiment with new Linux kernels
or distributions, and poke around in the internals of Linux, all
without risking your main Linux setup.

User-Mode Linux gives you a virtual machine that may have more hardware
and software virtual resources than your actual, physical computer. Disk
storage for the virtual machine is entirely contained inside a single
file on your physical machine. You can assign your virtual machine only
the hardware access you want it to have. With properly limited access,
nothing you do on the virtual machine can change or damage your real
computer, or its software.

%package    %{_target_cpu}
Group:		System/Kernel and hardware
Summary:	%{Summary}
Requires:   %{kname}-%{_target_cpu}-%{mdvkversion}

%description %{_target_cpu}
User-Mode Linux is a safe, secure way of running Linux versions and
Linux processes. Run buggy software, experiment with new Linux kernels
or distributions, and poke around in the internals of Linux, all
without risking your main Linux setup.

User-Mode Linux gives you a virtual machine that may have more hardware
and software virtual resources than your actual, physical computer. Disk
storage for the virtual machine is entirely contained inside a single
file on your physical machine. You can assign your virtual machine only
the hardware access you want it to have. With properly limited access,
nothing you do on the virtual machine can change or damage your real
computer, or its software.

%package    %{_target_cpu}-%{mdvkversion}
Group:		System/Kernel and hardware
Summary:	%{Summary}
Requires:   uml-utilities
Version:    1
Release:    1

%description %{_target_cpu}-%{mdvkversion}
User-Mode Linux is a safe, secure way of running Linux versions and
Linux processes. Run buggy software, experiment with new Linux kernels
or distributions, and poke around in the internals of Linux, all
without risking your main Linux setup.

User-Mode Linux gives you a virtual machine that may have more hardware
and software virtual resources than your actual, physical computer. Disk
storage for the virtual machine is entirely contained inside a single
file on your physical machine. You can assign your virtual machine only
the hardware access you want it to have. With properly limited access,
nothing you do on the virtual machine can change or damage your real
computer, or its software.

%package modules-%{mdvkversion}
Group:		System/Kernel and hardware
Summary:	Kernel module for UML kernel
AutoReqProv: No
Version:    1
Release:    1
Provides:   %{kname}-modules

%description modules-%{mdvkversion}
User-Mode Linux is a safe, secure way of running Linux versions and
Linux processes. Run buggy software, experiment with new Linux kernels
or distributions, and poke around in the internals of Linux, all
without risking your main Linux setup.

This package contains modules need inside the virtual machine when using
UML kernel compiled to use module.

This package has to be installed inside the VM, not on your system !

%prep
%setup -q -n linux-%{kversion}
%if %{?patchversion:1}%{?!patchversion:0}
%patch0 -p1
%endif
cp %SOURCE50 ./

%build
rm -rf $RPM_BUILD_ROOT

%__mkdir_p %buildroot/%_bindir

%if %bmodulesv
# Step 1: kernel w/ modules
cat %SOURCE1 | \
    sed 's/^CONFIG_LOCALVERSION=/CONFIG_LOCALVERSION="%{kernelversionappend}"/' \
    > .config

yes '' | %make oldconfig ARCH=um
%make modules linux ARCH=um

%make ARCH=um modules_install INSTALL_MOD_PATH=%buildroot
%__cp linux %buildroot/%_bindir/%name-mod-%{_target_cpu}-%mdvkversion
(
cd %buildroot/%_bindir
%__ln_s %name-mod-%{_target_cpu}-%mdvkversion linux-mod-%{_target_cpu}-%mdvkversion

%__ln_s %name-mod-%{_target_cpu}-%mdvkversion %name-mod-%{_target_cpu}
%__ln_s %name-mod-%{_target_cpu} linux-mod-%{_target_cpu}

%__ln_s %name-mod-%{_target_cpu} %name-mod
%__ln_s %name-mod linux-mod
)

cp .config config-mod-%{_target_cpu}-%mdvkversion

%make clean ARCH=um
rm -f .version
%endif

# Step 2: kernel w/o modules

cat %SOURCE1 | \
    sed 's/^CONFIG_LOCALVERSION=/CONFIG_LOCALVERSION="%{kernelversionappend}"/' | \
    sed 's/^CONFIG_MODULES.*/# CONFIG_MODULES is not set/' \
    > .config

yes '' | %make oldconfig ARCH=um
%make linux ARCH=um

%__cp linux %buildroot/%_bindir/%name-%{_target_cpu}-%mdvkversion
(
cd %buildroot/%_bindir
%__ln_s %name-%{_target_cpu}-%mdvkversion linux-%{_target_cpu}-%mdvkversion

%__ln_s %name-%{_target_cpu}-%mdvkversion %name-%{_target_cpu}
%__ln_s %name-%{_target_cpu} linux-%{_target_cpu}

%__ln_s %name-%{_target_cpu} %name
%__ln_s %name linux
)

cp .config config-%{_target_cpu}-%mdvkversion

%make clean ARCH=um
rm -f .version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.mdv
%_bindir/%name
%_bindir/linux
%if %bmodulesv
%_bindir/%name-mod
%_bindir/linux-mod
%endif

%files %{_target_cpu}
%defattr(-,root,root)
%doc README.mdv
%_bindir/%name-%{_target_cpu}
%_bindir/linux-%{_target_cpu}
%if %bmodulesv
%_bindir/%name-mod-%{_target_cpu}
%_bindir/linux-mod-%{_target_cpu}
%endif

%files %{_target_cpu}-%{mdvkversion}
%defattr(-,root,root)
%doc Documentation/uml
%doc README.mdv
%_bindir/%name-%{_target_cpu}-%mdvkversion
%_bindir/linux-%{_target_cpu}-%mdvkversion
%doc config-%{_target_cpu}-%mdvkversion
%if %bmodulesv
%_bindir/%name-mod-%{_target_cpu}-%mdvkversion
%_bindir/linux-mod-%{_target_cpu}-%mdvkversion
%doc config-mod-%{_target_cpu}-%mdvkversion
%endif

%if %bmodulesv
%files modules-%{mdvkversion}
%defattr(-,root,root)
%doc README.mdv
%doc config-mod-%{_target_cpu}-%mdvkversion
/lib/modules/*
%endif
