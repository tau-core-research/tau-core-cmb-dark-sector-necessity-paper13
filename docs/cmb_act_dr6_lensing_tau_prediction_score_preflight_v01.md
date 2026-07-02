# ACT DR6 Lensing Tau Prediction Score Preflight v01

**Doc class:** Tau-side prediction score preflight
**Status:** exact 18-bin Tau prediction input shape locked
**Canonical parent:** Paper 13 ACT DR6 lensing scoring route

This artifact converts the observed-side ACT DR6 lensing adapter into an exact
Tau-side input requirement. The required file is:

```text
data/score_ready_input/act_dr6_lensing_tau_prediction_vector_v01.csv
```

The file must contain 18 rows, one per ACT DR6 lensing bin, in the readout basis
`ACT_DR6_LENSING_BASELINE_18_BIN_CLKK`. The score can execute only if all rows
provide finite `tau_predicted_clkk` values and declare the endpoint-blind policy
`endpoint_blind_declared_no_observed_endpoint_fit`.

If the supplied source id is `tau_core_null_response_control_v01`, the resulting
score is a null-response control score only. It is not a physical Tau response
claim and cannot decide dark-sector necessity.

Summary:

```text
template_rows=18
prediction_file_present=True
prediction_rows=18
accepted_prediction_rows=18
score_executable_now=True
score_computed=True
chi2_tau=2129.1187283145146
chi2_per_naive_dof=118.28437379525081
next_required_artifact=none_score_computed_review_claim_boundary
```

## Claim Boundary

This preflight does not derive the Tau prediction vector. It only defines and
checks the exact score input shape. A later supplied vector must be justified by
a Tau-side derivation and must not be fitted to the observed endpoint.
