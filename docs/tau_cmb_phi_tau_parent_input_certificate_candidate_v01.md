# Tau CMB Phi Tau Parent Input Certificate Candidate v01

**Doc class:** parent-input certificate-candidate package
**Status:** certificate candidates declared but unpassed; no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_summary_v01.csv
```

This artifact declares certificate candidates for the parent-side base-field,
morphological seed, response operator, gauge/normalization metadata,
payload-firewall, and executable-replay rows. It does not pass any certificate
and accepts no parent-side Tau input.

The certificate candidate is not satisfied:

```text
certificate_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_audit_v01
```

## Claim Boundary

This artifact declares certificate candidates only. It supplies no dimension,
replay, or firewall certificate, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
