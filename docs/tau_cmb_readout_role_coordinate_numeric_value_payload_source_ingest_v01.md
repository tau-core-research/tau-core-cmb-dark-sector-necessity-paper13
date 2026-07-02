# Tau CMB Readout Role-Coordinate Numeric Value Payload Source Ingest v01

**Doc class:** focused protocol source ingest
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** CMB_READOUT_ROLE_COORDINATE_NUMERIC_VALUE_SOURCE_INGESTED_FOCUSED_PROTOCOL_BATCH_ONLY
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_v01_focused_protocol_sources_ingested_no_physical_CMB_score_no_likelihood_no_verdict
```

## Purpose

This step ingests the focused protocol source batch for `e_null`, the
`e_radiation` convention and stop-rule guards, the role-level
convention/stop/failure guards for `e_acoustic`, `e_density`, `e_lensing`, and
`e_growth`, plus the partial growth domain/codomain interface declarations. The
values are protocol/control values only, not physical CMB fit data. The physical
source terms, transfer kernels, response amplitudes, numeric bounds, and
inequalities remain blocked until concrete endpoint-blind values and provenance
are supplied.

## Summary

```text
source_ingest_rows=33
source_ingest_attempted_rows=17
source_ingested_rows=17
value_source_accepted_rows=17
protocol_value_score=0.515152
physical_CMB_score_allowed=False
likelihood_allowed=False
dark_sector_verdict_allowed=False
```

## Next Minimal Unblock

```text
tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance_audit_v01
```
