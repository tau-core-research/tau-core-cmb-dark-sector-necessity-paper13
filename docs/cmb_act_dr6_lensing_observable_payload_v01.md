# ACT DR6 Lensing Observable Payload v01

**Doc class:** observed CMB lensing payload
**Status:** local ACT DR6 lensing baseline bandpower payload extracted
**Canonical parent:** Paper 13 CMB source-data acquisition and scoring path

This artifact extracts a compact observable payload from the locally acquired
ACT DR6 lensing likelihood data package. It binds three local source files:
`clkk_bandpowers_act.txt`, `covmat_act.txt`, and `binning_matrix_act.txt`.

Summary:

```text
source_files_expected=3
source_files_present=3
source_files_hash_bound=3
bandpower_rows=18
covariance_shape=18x18
binning_matrix_shape=18x3000
shape_consistent=true
observable_payload_rows=18
accepted_observable_payload_rows=18
accepted_for_scoring_rows=0
```

## Claim Boundary

This is an observed-lensing payload only. It does not construct a Tau-side
prediction, does not run the ACT likelihood, does not compute a score, and does
not decide whether a dark-sector or no-dark-sector Tau Core route is required.
