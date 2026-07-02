# Tau CMB Seed Tau Payload Materialization Packet v01

**Doc class:** endpoint-blind seed payload materialization packet
**Status:** SEED_TAU_PAYLOAD_MATERIALIZATION_PACKET_TEMPLATE_DECLARED_UNPOPULATED

## Claim Boundary

```text
tau_cmb_seed_tau_payload_materialization_packet_v01_template_only_no_payload_values_no_payload_acceptance_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This artifact creates the narrow payload template needed by the seed readout
domain certificate. It does not populate seed values, accept a payload, certify
`seed_tau_CMB in Dom(R_CMB)`, evaluate a CMB readout, enter scoring, or decide
the Tau dark-sector question.

## Payload Template

```text
payload_templates/seed_tau_payload_TEMPLATE_v01.csv
sha256=e2263211d2647c23264fd4cd345805110210b6a525734441a44646fcb4f58194
```

The template is intentionally unpopulated. Any real payload must be built from
Tau-side morphology/readout sources only and must not read CMB endpoint
residuals, peak-shape fits, likelihood errors, score outputs, or post-endpoint
tuning fields.

## Packet Rows

- `TCMBSTPMP01_001` `seed_tau_payload.csv`: TEMPLATE_DECLARED_UNPOPULATED / PAYLOAD_NOT_ACCEPTED | blocks: template contains no populated seed values
- `TCMBSTPMP01_002` `seed_tau_payload.csv.provenance.json`: REQUIRED_NOT_MATERIALIZED / PROVENANCE_NOT_ACCEPTED | blocks: no provenance file is materialized for a populated payload
- `TCMBSTPMP01_003` `seed_tau_payload.csv.replay.txt`: REQUIRED_NOT_MATERIALIZED / REPLAY_NOT_ACCEPTED | blocks: no replay file is materialized for a populated payload
- `TCMBSTPMP01_004` `seed_tau_payload.csv.hashes.json`: REQUIRED_NOT_MATERIALIZED / HASHES_NOT_ACCEPTED | blocks: no hash manifest binds populated artifacts
- `TCMBSTPMP01_005` `seed_tau_payload.csv.firewall.json`: REQUIRED_NOT_MATERIALIZED / FIREWALL_NOT_ACCEPTED | blocks: no endpoint-blind firewall evidence is materialized
- `TCMBSTPMP01_006` `tau_cmb_seed_zero_control_v01`: REQUIRED_NOT_MATERIALIZED / ZERO_CONTROL_NOT_ACCEPTED | blocks: zero/null seed control is not defined

## Status

```text
SEED_TAU_PAYLOAD_MATERIALIZATION_PACKET_TEMPLATE_DECLARED_UNPOPULATED
```

This is the first place where the route becomes operationally concrete: the
next step is no longer to add another broad proof packet, but to populate the
declared payload and evidence files under the endpoint-blind firewall.

## Next Minimal Unblock

```text
populate_seed_tau_payload_from_tau_side_sources_only
```
