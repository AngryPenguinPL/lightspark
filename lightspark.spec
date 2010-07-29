Name: lightspark
Version: 0.4.2.2
Release: %mkrel 1
Summary: An alternative Flash Player implementation
Group: Networking/WWW
License: LGPLv3+
URL: http://lightspark.sourceforge.net
Source: http://edge.launchpad.net/lightspark/trunk/%name-%version/+download/%name-%version.tar.gz
Patch0: lightspark-0.4.2.2-link.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake
BuildRequires: llvm >= 2.7
BuildRequires: glew-devel >= 1.5.4
BuildRequires: ftgl-devel
BuildRequires: ffmpeg-devel
BuildRequires: nasm
BuildRequires: libSDL-devel
BuildRequires: gtkglext-devel
BuildRequires: pulseaudio-devel
BuildRequires: fontconfig-devel
BuildRequires: pcre-devel
BuildRequires: xulrunner-devel
BuildRequires: curl-devel

%description
Lightspark is a modern, free, open-source flash player implementation.
Lightspark features:

* JIT compilation of Actionscript to native x86 bytecode using LLVM
* Hardware accelerated rendering using OpenGL Shaders (GLSL)
* Very good and robust support for current-generation Actionscript 3
* A new, clean, codebase exploiting multithreading and optimized for 
modern hardware. Designed from scratch after the official Flash 
documentation was released.

%package mozilla-plugin
Summary: Mozilla compatible plugin for %{name}
Requires: mozilla-filesystem gnash
Group: Networking/WWW

%description mozilla-plugin
This is the Mozilla compatible plugin for %{name}

%prep
%setup -q
%patch0 -p0

%build
%cmake -DCOMPILE_PLUGIN=1  \
       -DPLUGIN_DIRECTORY="%{_libdir}/mozilla/plugins/" \
       -DENABLE_SOUND=1
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -C build

#remove devel file from package
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.so

install -Dpm 644 media/%{name}-ico.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
install -Dpm 644 media/%{name}-logo.svg $RPM_BUILD_ROOT%{_datadir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat <<EOF >$RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Name=Lightspark
Comment=An alternative flash player
TryExec=lightspark
Exec=lightspark
Icon=lightspark
NoDisplay=true
Type=Application
Categories=GNOME;GTK;AudioVideo;Video;Player;
MimeType=application/x-shockwave-flash;application/futuresplash;
StartupNotify=true
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER ChangeLog
%{_bindir}/%{name}
%{_bindir}/tightspark
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/man/man1/%{name}.1.*
%{_libdir}/%{name}

%files mozilla-plugin
%defattr(-,root,root,-)
%{_libdir}/mozilla/plugins/lib%{name}plugin.so
