%define	name	kernel-uml

%define	version	2.6.25
%define	release	%mkrel 1

%define	Summary	The user mode linux kernel

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Kernel and hardware

Source0:	linux-%{version}.tar.bz2
Source1:	%{name}-config.bz2
License:	GPL
Url:		http://user-mode-linux.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	glibc-static-devel
BuildRequires:  pcap-devel

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

%prep
%setup -q -n linux-%{version}
bzcat %SOURCE1 > .config

%build
yes '' | %make oldconfig ARCH=um
make linux ARCH=um

%install
rm -rf $RPM_BUILD_ROOT
%__mkdir_p %buildroot/%_bindir

%__cp linux %buildroot/%_bindir/%name-%version-%release
cd %buildroot/%_bindir
%__ln_s %name-%version-%release %name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Documentation/uml
%_bindir/%name
%_bindir/%name-%version-%release

