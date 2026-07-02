# Tau CMB Phi Tau Parent Input Evidence Payload Acceptance Decision Gate v01

**Doc class:** parent-input evidence payload acceptance decision gate
**Status:** acceptance decision gate closed because unblock plan is not completed; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_summary_v01.csv
```

This artifact applies the payload acceptance decision rule after the acceptance
unblock plan. The unblock plan is not completed, so acceptance remains closed.

The evidence payload acceptance decision gate is not satisfied:

```text
evidence_payload_acceptance_decision_gate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01
```

## Claim Boundary

This artifact applies an acceptance decision gate only. It materializes no
parent-side payload, validates no receipt, accepts no receipt, provides no
evidence-package pass, provides no certificate pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
