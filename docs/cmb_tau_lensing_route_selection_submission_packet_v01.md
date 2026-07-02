# CMB Tau Lensing Route Selection Submission Packet v01

**Doc class:** submission packet
**Reader role:** Paper 13 scoring implementer
**Status:** no route submitted
**Canonical parent:** `docs/cmb_tau_lensing_numeric_grid_route_selection_gate_v01.md`

This packet defines how an allowed numeric-grid route may be submitted.

## Allowed Submissions

Submit exactly one of:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

## Direct Route Files

```text
payloads/tau_lensing_response_pp_grid_v01.csv
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

## Delta Route Files

```text
payloads/tau_lensing_response_delta_pp_v01.csv
payloads/tau_lensing_response_fiducial_pp_reference_v01.json
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

## Failure Route File

```text
payloads/tau_lensing_response_grid_failure_statement_v01.md
```

## Forbidden

```text
posthoc_or_template_grid
```

## Claim Boundary

```text
route_selection_submission_packet_only_no_selected_route_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
