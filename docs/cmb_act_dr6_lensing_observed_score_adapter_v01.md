# ACT DR6 Lensing Observed Score Adapter v01

**Doc class:** observed-side score adapter
**Status:** observed vector and covariance adapter locked; Tau prediction absent
**Canonical parent:** Paper 13 ACT DR6 lensing payload route

This artifact freezes the observed-side reduced score adapter for the ACT DR6
lensing baseline payload. It defines the score expression

```text
chi2_tau = (y_obs - y_tau)^T C_obs^-1 (y_obs - y_tau)
```

where `y_obs` is the 18-bin ACT DR6 lensing convergence bandpower vector and
`y_tau` must be a Tau-side prediction vector in the same 18-bin readout basis.

Summary:

```text
observed_payload_rows=18
covariance_shape=[18, 18]
inverse_covariance_shape=[18, 18]
covariance_symmetric=True
covariance_positive_definite=True
covariance_condition_number=841.941478991
tau_prediction_required_shape=[18]
tau_prediction_rows_present=0
score_executable_now=false
```

## Claim Boundary

This is an observed-side adapter only. It does not provide `y_tau`, does not run
the ACT likelihood, does not compute a Tau score, and does not decide dark-sector
necessity.
