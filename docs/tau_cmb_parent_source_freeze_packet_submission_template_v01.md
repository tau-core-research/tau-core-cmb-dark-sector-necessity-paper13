# Tau CMB Parent-Source Freeze Packet Submission Template v01

**Doc class:** endpoint-blind freeze-packet submission template
**Status:** template declared; no payload submitted, no source accepted, no score

## Claim Boundary

```text
tau_cmb_parent_source_freeze_packet_submission_template_v01_template_only_no_payload_submitted_no_source_acceptance_no_phi_derivation_no_score_no_verdict
```

## Purpose

This artifact provides the concrete CSV shape for submitting a populated CMB
parent-source freeze packet. It is a template only. It does not submit values,
accept a source, derive `Phi_tau_eff`, or open scoring.

Template:

```text
payload_templates/tau_cmb_parent_source_freeze_packet_submission_TEMPLATE_v01.csv
```

The required populated fields are:

```text
packet_id
B_tau_base_CMB_descriptor
seed_tau_CMB_descriptor
R_tau_CMB_input_set
gauge_norm_tau_CMB_metadata
source_freeze_firewall_certificate
freeze_packet_replay_rule
```

Each populated row must include provenance, replay information, an artifact
hash, dimensional/unit status where applicable, and an endpoint-exclusion
statement.

A reproducible negative candidate may be materialized at:

```text
payloads/tau_cmb_parent_source_freeze_packet_submission_candidate_v01.csv
```

## Status

```text
PARENT_SOURCE_FREEZE_PACKET_SUBMISSION_TEMPLATE_DECLARED_UNPOPULATED
```

## Next Minimal Unblock

```text
submit_populated_endpoint_blind_parent_source_freeze_packet_candidate
```
