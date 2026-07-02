# Tau CMB Phi Tau Parent Input Evidence Payload Acceptance Precheck v01

**Doc class:** parent-input evidence payload acceptance precheck
**Status:** acceptance precheck declared but failed because materialization audit is not satisfied; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_summary_v01.csv
```

This artifact checks whether parent-side evidence payload packets are eligible
for acceptance. The materialization audit is not satisfied, so no payload is accepted.

The evidence payload acceptance precheck is not satisfied:

```text
evidence_payload_acceptance_precheck_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01
```

## Claim Boundary

This artifact performs an acceptance precheck only. It materializes no
parent-side payload, validates no receipt, accepts no receipt, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
