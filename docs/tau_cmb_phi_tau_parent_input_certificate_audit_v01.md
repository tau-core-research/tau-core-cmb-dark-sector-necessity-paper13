# Tau CMB Phi Tau Parent Input Certificate Audit v01

**Doc class:** parent-input certificate-candidate audit
**Status:** candidate certificates audited and rejected for scoring acceptance; no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_summary_v01.csv
```

This artifact audits the seven certificate candidates declared in
`tau_cmb_phi_tau_parent_input_certificate_candidate_v01`.
All seven candidates fail the audit because no certificate evidence is supplied.

The certificate audit is not satisfied:

```text
certificate_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_certificate_closure_decision_v01
```

## Claim Boundary

This artifact audits certificate candidates only. It supplies no dimension,
replay, or firewall certificate, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
