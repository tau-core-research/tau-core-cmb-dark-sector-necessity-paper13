# Tau CMB Phi Tau Parent Input Dimension Replay Certificate v01

**Doc class:** dimension/replay/firewall certificate requirements
**Status:** certificate requirements declared but unsupplied; no certificate, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_dimension_replay_certificate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_summary_v01.csv
```

This artifact declares the certificate requirements needed after the
payload-firewall audit: dimension or unit certificates, executable replay
certificates, and payload-level firewall certificates.
It supplies no certificate package and accepts no parent-side Tau input.

The dimension/replay certificate is not satisfied:

```text
dimension_replay_certificate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_candidate_v01
```

## Claim Boundary

This artifact declares certificate requirements only. It supplies no dimension,
replay, or firewall certificate, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
