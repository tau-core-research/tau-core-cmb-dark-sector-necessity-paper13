# CMB Tau Lensing Response Payload Acceptance Audit v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** payload acceptance audit, payload absent
**Canonical parent:** `docs/cmb_tau_lensing_response_payload_submission_packet_v01.md`

This audit checks whether the response-vector payload required for Tau lensing
scoring has actually been submitted.

## Result

No required payload file is present.

The audit therefore rejects the current state as a scoring input. This is a
controlled blocker, not a failed Tau Core score.

## Missing Files

```text
tau_lensing_response_pp_grid_v01.csv
tau_lensing_response_delta_pp_v01.csv
tau_lensing_response_parameter_policy_v01.csv
tau_lensing_response_payload_provenance_v01.json
tau_lensing_response_payload_hashes_v01.json
tau_lensing_response_firewall_v01.md
tau_lensing_response_claim_boundary_v01.md
```

At least one of the two numeric vector files must be submitted, and all required
supporting files must be supplied before a Tau response vector can be accepted.

## Decision

```text
REJECT_FOR_SCORING_INPUT
```

No payload is accepted. No Tau score is allowed.

## Next Gate

The next useful gate is a payload template packet that creates empty, clearly
marked templates for the required files. Templates must not be accepted as
payloads.

## Claim Boundary

```text
payload_acceptance_audit_only_no_payload_accepted_no_tau_score_no_dark_sector_verdict
```

The payload template packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_response_payload_template_packet_v01.csv
docs/cmb_tau_lensing_response_payload_template_packet_v01.md
payload_templates/
```
