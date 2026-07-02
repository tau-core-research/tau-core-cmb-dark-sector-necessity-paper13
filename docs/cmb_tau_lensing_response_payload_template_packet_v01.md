# CMB Tau Lensing Response Payload Template Packet v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** template packet, not payload
**Canonical parent:** `docs/cmb_tau_lensing_response_payload_acceptance_audit_v01.md`

This packet provides empty templates for the Tau lensing response payload. The
templates are intentionally marked:

```text
TEMPLATE_NOT_PAYLOAD
```

They must not be accepted as scoring input.

## Template Files

```text
payload_templates/tau_lensing_response_pp_grid_v01.csv
payload_templates/tau_lensing_response_delta_pp_v01.csv
payload_templates/tau_lensing_response_parameter_policy_v01.csv
payload_templates/tau_lensing_response_payload_provenance_v01.json
payload_templates/tau_lensing_response_payload_hashes_v01.json
payload_templates/tau_lensing_response_firewall_v01.md
payload_templates/tau_lensing_response_claim_boundary_v01.md
```

## Submission Rule

A real payload must be copied or generated outside `payload_templates/`, must
remove the `TEMPLATE_NOT_PAYLOAD` marker, and must pass the acceptance audit
before any Tau score attempt.

At least one numeric vector file is required:

```text
tau_lensing_response_pp_grid_v01.csv
```

or:

```text
tau_lensing_response_delta_pp_v01.csv
```

## Claim Boundary

```text
payload_template_packet_only_no_payload_no_tau_score_no_dark_sector_verdict
```

The derivation route from Tau CMB source slots to payload templates is tracked
at:

```text
data/source_manifest/cmb_tau_lensing_response_derivation_route_v01.csv
docs/cmb_tau_lensing_response_derivation_route_v01.md
```
