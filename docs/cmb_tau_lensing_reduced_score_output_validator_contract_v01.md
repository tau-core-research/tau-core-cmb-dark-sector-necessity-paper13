# CMB Tau Lensing Reduced Score Output Validator Contract v01

**Doc class:** score-output validator contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, waiting for score output
**Canonical parent:** `docs/cmb_tau_lensing_reduced_score_output_schema_lock_v01.md`

This contract registers the reduced score output validator:

```text
scripts/validate_tau_lensing_reduced_score_output.py
```

## What It Validates

```text
required fields only
claim_boundary is locked
projected_shape == [18]
naive_dof == 18
likelihood_run == false
dark_sector_verdict == false
```

## What It Does Not Do

```text
no score computation
no likelihood
no dark-sector verdict
```

## Smoke Tests

```text
valid reduced-score schema: pass
dark_sector_verdict=true: rejected
```

## Claim Boundary

```text
reduced_score_output_validator_contract_only_no_score_output_no_dark_sector_verdict
```
