# CMB Tau Lensing Scoring Environment Contract v01

**Doc class:** scoring-environment contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented
**Canonical parent:** `docs/cmb_lensing_reduced_score_adapter_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_scoring_environment_contract_v01.csv`

This contract checks the ACT-side files required by the reduced Tau lensing
score. It does not check any Tau grid, does not run a score, and does not issue
a dark-sector verdict.

## Command

```text
make env-check
```

Default generated report:

```text
data/derived/cmb_tau_lensing_scoring_environment_report_v01.json
```

## Checked Inputs

```text
binning_matrix_act.txt: shape (18, 3000)
clkk_bandpowers_act.txt: shape (18,)
covmat_act.txt: shape (18, 18), symmetric, positive eigenvalues
```

## Claim Boundary

```text
scoring_environment_contract_only_no_tau_grid_no_score_no_dark_sector_verdict
```
