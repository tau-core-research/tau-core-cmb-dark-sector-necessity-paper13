# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Candidate v01

**Doc class:** parent-input evidence payload scoring input candidate
**Status:** scoring input candidates declared but not accepted; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_summary_v01.csv
```

This artifact declares scoring input candidates that would be constructed from
accepted endpoint-blind evidence payloads. The acceptance decision gate is
closed, so no scoring input is accepted.

The evidence payload scoring input candidate is not satisfied:

```text
evidence_payload_scoring_input_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01
```

## Claim Boundary

This artifact declares scoring-input candidates only. It accepts no
parent-side payload, provides no evidence-package pass, provides no certificate
pass, accepts no scoring input, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
