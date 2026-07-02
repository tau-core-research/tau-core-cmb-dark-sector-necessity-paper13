# CMB Tau Lensing Reduced Score Output Schema Lock v01

**Doc class:** score schema lock
**Reader role:** Paper 13 scoring implementer
**Status:** schema locked, score not run
**Canonical parent:** `docs/cmb_tau_lensing_reduced_score_runner_contract_v01.md`

This lock fixes the only acceptable output schema for a future reduced Tau
lensing score run.

## Required Fields

```text
report_id
claim_boundary
route_id
grid_sha256
projected_shape
chi2_tau
naive_dof
chi2_per_naive_dof
likelihood_run
dark_sector_verdict
```

## Required Claim Boundary

```text
reduced_tau_lensing_score_only_no_likelihood_no_dark_sector_verdict
```

## Hard Locks

```text
likelihood_run: false
dark_sector_verdict: false
projected_shape: [18]
```

## Claim Boundary

```text
reduced_score_output_schema_lock_only_no_score_run_no_dark_sector_verdict
```
