# Tau CMB Phi Tau Parent Input Populated Evidence Package Audit v01

**Doc class:** parent-input populated evidence package audit
**Status:** populated-package candidate audited and rejected; no evidence payload, no package pass, no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_populated_evidence_package_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_summary_v01.csv
```

This artifact audits the populated evidence package candidate. All seven rows
fail because the required payload records are declared but not supplied.

The populated evidence package audit is not satisfied:

```text
populated_evidence_package_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01
```

## Claim Boundary

This artifact audits required populated-package payload records only. It
supplies no dimension, replay, or firewall evidence payload, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
