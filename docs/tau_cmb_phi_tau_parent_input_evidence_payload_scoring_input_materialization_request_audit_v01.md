# Tau CMB Phi Tau Parent Input Evidence Payload Scoring Input Materialization Request Audit v01

**Doc class:** parent-input evidence payload scoring input materialization request audit
**Status:** materialization request audited but not fulfilled; no payload accepted, no package pass, no certificate pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_summary_v01.csv
```

This artifact audits the materialization request. The request exists and is
audited, but it is not fulfilled because no requested packet is materialized or
submitted.

The evidence payload scoring input materialization request audit is not
satisfied:

```text
evidence_payload_scoring_input_materialization_request_audit_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01
```

## Claim Boundary

This artifact is an audit only. It accepts no parent-side payload, provides no
evidence-package pass, provides no certificate pass, accepts no scoring input,
derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
