# Tau CMB Phi Tau Parent Input Certificate Evidence Request v01

**Doc class:** parent-input certificate evidence request
**Status:** evidence requirements declared but not supplied; no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_request.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_summary_v01.csv
```

This artifact converts the failed certificate audit into a concrete evidence
request. All seven rows request evidence, but no evidence is supplied in this
artifact.

The certificate evidence request is not satisfied:

```text
certificate_evidence_request_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01
```

## Claim Boundary

This artifact requests certificate evidence only. It supplies no dimension,
replay, or firewall evidence, provides no certificate pass, accepts no
parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score, supplies no
CMB likelihood, declares no reproduction or failure, validates no Tau-response
source, and permits no no-dark or dark-sector verdict.
