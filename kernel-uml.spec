%define kname   kernel-uml
%define	name	%{kname}

%define	kversion	2.6.26
#define patchversion 10

%define rpmversion %{kversion}%{?patchversion:.%{patchversion}}
%define	release	%mkrel 1

%define	Summary	The user mode linux kernel

Summary:	%{Summary}
Name:		%{name}
Version:	%{rpmversion}
Release:	%{release}
Group:		System/Kernel and hardware

Source0:	linux-%{kversion}.tar.bz2
Source1:	%{name}-config.bz2
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

%package    %{_target_cpu}-%{rpmversion}
Group:		System/Kernel and hardware
Version:    1
Summary:	%{Summary}
Requires:   uml-utilities

%description %{_target_cpu}-%{rpmversion}
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
Requires:   %{kname}-%{_target_cpu}-%{rpmversion} = 1-%{release}

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

%prep
%setup -q -n linux-%{kversion}
%if %{?patchversion:1}%{?!patchversion:0}
%patch0 -p1
%endif
bzcat %SOURCE1 > .config

%build
yes '' | %make oldconfig ARCH=um
make linux ARCH=um

%install
rm -rf $RPM_BUILD_ROOT
%__mkdir_p %buildroot/%_bindir

%__cp linux %buildroot/%_bindir/%name-%rpmversion-%{_target_cpu}
cd %buildroot/%_bindir
%__ln_s %name-%rpmversion-%{_target_cpu} %name
%__ln_s %name-%rpmversion-%{_target_cpu} %name-%{_target_cpu}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_bindir/%name

%files %{_target_cpu}
%defattr(-,root,root)
%_bindir/%name-%{_target_cpu}

%files %{_target_cpu}-%{rpmversion}
%defattr(-,root,root)
%doc Documentation/uml
%_bindir/%name-%rpmversion-%{_target_cpu}

