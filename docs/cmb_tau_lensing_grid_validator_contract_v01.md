# CMB Tau Lensing Grid Validator Contract v01

**Doc class:** validator contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, waiting for real grid payload
**Canonical parent:** `docs/cmb_tau_lensing_numeric_grid_materialization_request_v01.md`

This contract registers the validator for future `tau_PP_grid` or
`delta_PP_tau` payloads:

```text
scripts/validate_tau_lensing_grid_payload.py
```

## What It Checks

- rejects files marked `TEMPLATE_NOT_PAYLOAD`;
- requires exactly 3000 finite numeric values;
- if two numeric columns are supplied, requires the first column to be exactly
  `L = 10..3009`;
- records grid file hash and value hash;
- preserves the fixed alignment `L = 10 + i`;
- optionally replays `B_ACT @ grid -> shape (18,)`;
- optionally writes a replay JSON with hashes.

## What It Does Not Do

```text
no chi2
no likelihood
no Tau score
no dark-sector verdict
```

## Negative Test

The validator was run against the template PP-grid file and correctly rejected
it as `TEMPLATE_NOT_PAYLOAD`.

## Claim Boundary

```text
grid_validator_contract_only_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
