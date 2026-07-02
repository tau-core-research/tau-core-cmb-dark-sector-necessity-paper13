# CMB Tau Lensing Reduced Score Runner Contract v01

**Doc class:** score-runner contract
**Reader role:** Paper 13 scoring implementer
**Status:** runner implemented, score not run
**Canonical parent:** `docs/cmb_tau_lensing_prescore_readiness_lock_v01.md`

This contract registers the reduced ACT lensing score runner:

```text
scripts/run_tau_lensing_reduced_score.py
```

## Required Input

The runner requires a validator projection replay:

```text
payloads/tau_lensing_pp_grid_projection_replay_v01.json
```

The replay must have:

```text
score_computed: false
dark_sector_verdict: false
projected_shape: [18]
```

## What It Computes

Only the reduced diagnostic quantity:

```text
chi2_tau = (y_ACT - B_ACT tau_PP)^T C_ACT^-1 (y_ACT - B_ACT tau_PP)
```

## What It Does Not Claim

```text
no full likelihood
no parameter inference
no dark-sector verdict
no Tau Core validation
```

## Claim Boundary

```text
reduced_score_runner_contract_only_no_score_run_no_dark_sector_verdict
```
