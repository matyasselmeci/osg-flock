Name:      ospool-ap
Version:   1.10
Release:   2%{?dist}
Summary:   OSPool Access Point configurations

License:   Apache 2.0
URL:       https://opensciencegrid.org/docs/submit/ospool-ap

BuildArch: noarch

Requires(post): gratia-probe-condor-ap
BuildRequires: condor
Requires: condor

Obsoletes: osg-flock <= %{version}
Provides: osg-flock = %{version}

Source0: %{name}-%{version}%{?gitrev:-%{gitrev}}.tar.gz

%description
%{summary}

%prep
%setup -q

%build

%install
rm -fr $RPM_BUILD_ROOT

# Install condor configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d
install -m 644 rpm/80-osg-flocking.conf $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d

# Advertise package version so we can easily track at the cm
echo > $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d/81-osg-flock-version.conf \
'# THIS FILE IS AUTOGENERATED; DO NOT EDIT
OSG_FLOCK_VERSION = "%{version}"
SCHEDD_ATTRS = $(SCHEDD_ATTRS) OSG_FLOCK_VERSION
'

# Install gratia configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gratia/condor/

%post
# Set OSPool specific Gratia probe config
probeconfig=/etc/gratia/condor-ap/ProbeConfig
overrides=(
    'VOOverride="osg"'
)

for override in "${overrides[@]}"; do
    if grep "$override" $probeconfig 2>&1 > /dev/null; then
        # override already present
        continue
    else
        # add override if not present
        sed -i -e "s/\(EnableProbe.*\)/\1\n    $override/" $probeconfig
    fi
done

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%config(noreplace) %{_sysconfdir}/condor/config.d/80-osg-flocking.conf
%config %{_sysconfdir}/condor/config.d/81-osg-flock-version.conf


%changelog
* Mon Oct 21 2024 Matt Westphall <westphall@wisc.edu> - 1.10-2
- Initial release as ospool-ap

* Thu Jun 20 2024 Mats Rynge <rynge@isi.edu> - 1.10-1
- Add extra attributes for transfer ads (OSPOOL-123)

* Tue Feb 21 2023 Mats Rynge <rynge@isi.edu> - 1.9-1
- Add OSPool attribute to the job ad from the EP config (SOFTWARE-4803)

* Mon Apr 18 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.8-1
- Include the package version in the schedd classad (SOFTWARE-5105)
- Disable .sif images on 3.x kernels (OSPOOL-18)
- Improve OS_VERSION handling
- Drop Map* ProbeConfig overrides (SOFTWARE-5042)

* Thu Dec 2 2021 Mats Rynge <rynge@isi.edu> 1.7-1
- Moved to the new ospool.osg-htc.org central managers in high
  availability setup
- Removed pre-9.0 HTCondor config - this is no longer
  supported by the OSPool (IDTOKENS only)
- Change the VO override to the lowercase "osg" (SOFTWARE-4905)

* Thu Nov 4 2021 Brian Lin <blin@cs.wisc.edu> 1.6-3
- Append OSPool specific ProbeConfig changes in post-installation
  (SOFTWARE-4846)

* Wed Oct 27 2021 Brian Lin <blin@cs.wisc.edu> 1.6-2
- Remove reference to old ProbeConfig

* Mon Oct 25 2021 Mats Rynge <rynge@isi.edu> 1.6-1
- Now requires gratia-probe-condor-ap, probe config has been removed

* Fri Oct 1 2021 Mats Rynge <rynge@isi.edu> 1.5-1
- Moved to new HTCondor Cron Gratia setup

* Wed Sep 29 2021 Mats Rynge <rynge@isi.edu> 1.4-1
- Updating for OSG 3.6, idtoken auth

* Fri Jan 1 2021 Mats Rynge <rynge@isi.edu> 1.3-1
- Enable Schedd AuditLog by default in osg-flock (SOFTWARE-4390)

* Fri Oct 23 2020 Brian Lin <blin@cs.wisc.edu> 1.2-2
- Fix paths to configuration source files

* Thu Oct 22 2020 Mats Rynge <rynge@isi.edu> 1.2-1
- Moved to IDTOKENS on HTCondor versions greater than 8.9.6

* Mon Jun 8 2020 Brian Lin <blin@cs.wisc.edu> 1.1-2
- Fix CA requirements to work with osg-ca-scripts or certificate bundles

* Wed Apr 10 2019 Brian Lin <blin@cs.wisc.edu> 1.1-1
- Add new OSG flock host certificate DN (SOFTWARE-3603)

* Fri Sep 07 2018 Suchandra Thapa <ssthapa@uchicago.edu> 1.0-1
- Initial meta package based in part on osg-condor-flock rpms

