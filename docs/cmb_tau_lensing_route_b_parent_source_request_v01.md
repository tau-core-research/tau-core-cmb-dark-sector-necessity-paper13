# CMB Tau Lensing Route B Parent Source Request v01

**Doc class:** endpoint-blind Route B parent-source fulfillment request
**Status:** request only; no parent source, no grid, no score, no verdict
**Canonical script:** `scripts/build_tau_lensing_route_b_parent_source_request.py`
**Canonical parent:** `docs/cmb_tau_lensing_physical_candidate_upstream_request_v01.md`

This document narrows the Tau-grid blocker to the first concrete Route B
object that must be supplied: a Tau-derived parent-source L-table and its
non-template materialization config.

## Required Files

```text
payload_staging/tau_lensing_route_b_parent_source_v01.csv
payload_staging/tau_lensing_route_b_parent_source_config_v01.json
```

## Parent Source Table

```text
L,parent_tau_source_value
10,<finite Tau-derived value>
...
3009,<finite Tau-derived value>
```

The table must contain exactly 3000 rows with integer `L=10..3009`.
`parent_tau_source_value` must be finite and non-template. It must not be
a diagnostic probe or a zero-control promoted as a physical Tau response.

## Config Contract

Required fields:
- `config_id`
- `selected_route`
- `response_rule`
- `parent_source_table`
- `parent_l_column`
- `parent_value_column`
- `normalization`
- `endpoint_blind_statement`
- `parameter_policy`
- `source_chain`
- `normalization_statement`
- `known_limit_statement`
- `claim_boundary`

Fixed values:
- `selected_route` = `delta_PP_tau_against_named_fiducial_PP`
- `response_rule` = `linear_parent_source_v01`
- `parent_l_column` = `L`
- `parent_value_column` = `parent_tau_source_value`

## Required Evidence

- parent_tau_source(L) is derived from Tau-side morphology/source structure before endpoint score readout
- source_chain names the derivation artifacts or scripts that generated the table
- normalization is finite and fixed before any score, residual, or verdict inspection
- known-limit statement verifies parent_tau_source_value -> 0 implies delta_PP_tau -> 0
- parameter_policy excludes ACT/Planck residual fitting, reduced chi2 tuning, score tuning, and verdict preference
- replay command or generator is identified so the table can be regenerated

## Forbidden Inputs

- ACT residuals
- Planck residuals
- reduced chi2 tuning
- score output tuning
- dark-sector verdict preference
- diagnostic probe parameters
- zero-control definitions promoted as physical response
- template placeholders

## Materialization Rule

```text
delta_PP_tau(L)=normalization*parent_tau_source_value(L) for response_rule=linear_parent_source_v01
```

This rule is only an adapter from an already justified Tau parent source
into the upstream L-response format. It does not prove the parent source.

## Acceptance Commands

```text
make tau-grid-route-b-parent-table-precheck
make tau-grid-route-b-parent-dry-run
make tau-grid-route-b-parent-write-staging
make tau-grid-derivation-intake-audit
make tau-grid-physical-candidate-precheck
make tau-grid-handoff-write-staging
make tau-grid-physical-candidate-package
make staging-promote-delta-dry-run
```

## Claim Boundary

```text
route_b_parent_source_request_only_no_parent_source_no_grid_no_score_no_dark_sector_verdict
```
