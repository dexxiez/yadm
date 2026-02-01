%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# rpkg macros for git-based builds
{{{ git_dir_vcs_tag }}}
%global commit_short {{{ git_short_commit }}}

Name: yadm-dexxiez
Summary: Yet Another Dotfiles Manager (dexxiez fork)
Version: 3.5.0
Release: 1.git%{commit_short}%{?dist}
URL: https://yadm.io
License: GPL-3.0-only
Requires: bash
Requires: git
Conflicts: yadm

# rpkg macro to create tarball from git
Source0: {{{ git_dir_pack }}}
BuildArch: noarch

%description
yadm is a tool for managing a collection of files across multiple computers,
using a shared Git repository. In addition, yadm provides a feature to select
alternate versions of files based on the operation system or host name. Lastly,
yadm supplies the ability to manage a subset of secure files, which are
encrypted before they are included in the repository.

%prep
# rpkg macro to extract the git-generated tarball
{{{ git_dir_setup_macro }}}

%build

%install


%{__mkdir} -p %{buildroot}%{_bindir}
%{__cp}  yadm %{buildroot}%{_bindir}
sed -i 's/VERSION=REPLACEONBUILD/VERSION="%{version}-git%{commit_short}%{?dist}"/' %{buildroot}%{_bindir}/yadm

%{__mkdir} -p  %{buildroot}%{_mandir}/man1
%{__cp} yadm.1 %{buildroot}%{_mandir}/man1

%{__mkdir} -p                        %{buildroot}%{_pkgdocdir}
%{__cp} README.md                    %{buildroot}%{_pkgdocdir}/README
%{__cp} CHANGES CONTRIBUTORS LICENSE %{buildroot}%{_pkgdocdir}
%{__cp} -r contrib                   %{buildroot}%{_pkgdocdir}

%files
%attr(755,root,root) %{_bindir}/yadm
%attr(644,root,root) %{_mandir}/man1/*
%doc %{_pkgdocdir}
