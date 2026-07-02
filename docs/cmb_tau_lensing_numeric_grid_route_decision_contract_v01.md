# CMB Tau Lensing Numeric Grid Route Decision Contract v01

**Doc class:** route contract
**Reader role:** Paper 13 scoring implementer
**Status:** route options declared, no grid payload
**Canonical parent:** `docs/cmb_tau_lensing_numeric_grid_candidate_audit_v01.md`

This contract fixes the allowed ways a numeric CMB lensing PP-grid payload may
enter the reduced scoring path.

## Allowed Routes

Exactly one route must be chosen before score evaluation:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

## Direct Route

Requires:

```text
payloads/tau_lensing_response_pp_grid_v01.csv
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

The grid must contain exactly 3000 finite values under `L = 10 + i`.

## Delta Route

Requires:

```text
payloads/tau_lensing_response_delta_pp_v01.csv
payloads/tau_lensing_response_fiducial_pp_reference_v01.json
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

The total grid is formed only by the predeclared rule:

```text
tau_PP_grid_total(L) = fiducial_PP_named(L) + delta_PP_tau(L)
```

## Failure Route

If no endpoint-blind numeric grid can be derived, the correct result is an
explicit failure statement, not a fitted substitute:

```text
payloads/tau_lensing_response_grid_failure_statement_v01.md
```

## Forbidden Route

The following are never accepted as Tau scoring inputs:

```text
template grid
ACT residual fitted curve
Planck residual fitted curve
reduced-chi2 tuned response
post-hoc dark-sector verdict driven response
```

## Claim Boundary

```text
numeric_grid_route_decision_contract_only_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
