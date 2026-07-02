# Tau Lensing Response Grid Route Declaration TEMPLATE v01

**Status:** TEMPLATE_NOT_PAYLOAD
**Purpose:** fill this only when submitting a real numeric grid route.

## Selected Route

Choose exactly one:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

## Required Statement

Direct route block:

```text
selected_route: direct_tau_PP_grid
numeric_grid_file: payloads/tau_lensing_response_pp_grid_v01.csv
fiducial_reference_file: not_used
provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json
index_alignment: L = 10 + i
endpoint_blind_statement:
```

Delta route block:

```text
selected_route: delta_PP_tau_against_named_fiducial_PP
numeric_grid_file: payloads/tau_lensing_response_delta_pp_v01.csv
fiducial_reference_file: payloads/tau_lensing_response_fiducial_pp_reference_v01.json
provenance_file: payloads/tau_lensing_response_grid_provenance_v01.json
index_alignment: L = 10 + i
endpoint_blind_statement:
```

Failure route block:

```text
selected_route: explicit_failure_no_endpoint_blind_grid
numeric_grid_file: not_used
fiducial_reference_file: not_used
provenance_file: not_used
index_alignment: not_used
endpoint_blind_statement: no endpoint-blind numeric grid can be submitted
```

Generic field list:

```text
selected_route:
numeric_grid_file:
fiducial_reference_file: not_used_or_path
provenance_file:
index_alignment: L = 10 + i
endpoint_blind_statement:
```

## Forbidden Construction

The route must not be selected from:

```text
ACT residuals
Planck residuals
reduced chi2
dark-sector verdict preference
```

## Claim Boundary

```text
route_declaration_template_only_not_payload_no_tau_score_no_dark_sector_verdict
```
