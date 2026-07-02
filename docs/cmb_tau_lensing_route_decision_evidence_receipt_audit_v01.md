# CMB Tau Lensing Route Decision Evidence Receipt Audit v01

**Doc class:** evidence receipt audit
**Reader role:** Paper 13 scoring implementer
**Status:** evidence not received
**Canonical parent:** `docs/cmb_tau_lensing_route_decision_evidence_request_v01.md`

This audit checks whether any requested route-decision evidence file exists in
`payloads/`.

## Decision

```text
ROUTE_EVIDENCE_RECEIPT_BLOCKED
```

No requested route evidence has been received.

## Missing Evidence Sets

Direct route:

```text
payloads/tau_lensing_response_pp_grid_v01.csv
payloads/tau_lensing_response_grid_provenance_v01.json
payloads/tau_lensing_response_grid_route_declaration_v01.md
```

Delta route:

```text
payloads/tau_lensing_response_delta_pp_v01.csv
payloads/tau_lensing_response_fiducial_pp_reference_v01.json
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

Failure route:

```text
payloads/tau_lensing_response_grid_failure_statement_v01.md
```

## Claim Boundary

```text
route_decision_evidence_receipt_audit_only_no_evidence_received_no_selected_route_no_tau_score_no_dark_sector_verdict
```
