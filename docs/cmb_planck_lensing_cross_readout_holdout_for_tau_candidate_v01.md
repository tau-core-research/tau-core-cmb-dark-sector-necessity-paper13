# Planck Lensing Cross-Readout Holdout for Tau Candidate v01

**Doc class:** cross-readout holdout diagnostic
**Status:** ACT-selected nonzero Tau-shape candidate transferred unchanged to the Planck lensing block
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact tests whether the best ACT-screened nonzero Tau Core-style
lensing response control remains useful when transferred unchanged to the
Planck lensing bandpower block distributed in the same ACT DR6 lensing package.
The candidate parameters are not refitted to Planck.

The Planck-only diagnostic covariance is taken as the bottom-right \(9\times9\)
block of `covmat_actplanck.txt`, corresponding to the 18 ACT rows followed by
the 9 Planck rows. This is a reduced cross-readout diagnostic, not a full
Planck likelihood evaluation.

Summary:

```text
planck_rows=9
planck_covariance_shape=9x9_from_bottom_right_block_of_27x27_actplanck_covariance
planck_covariance_positive_definite=True
candidate_id=tau_shape_control_morph_lensing_broad_lowL_A1e-07
transferred_amplitude=1e-07
transferred_ell_c=120.0
transferred_rise_power=0.5
transferred_fall_power=1.0
null_chi2=1974.9220116735582
candidate_chi2=307.71562329316146
candidate_delta_chi2_vs_null=1667.2063883803967
candidate_fractional_chi2_improvement_vs_null=0.8441884684689893
obligation_NZRESP_OBL_004_status=partially_addressed_by_planck_cross_readout_diagnostic_not_closed
```

## Claim Boundary

This artifact supports only a holdout diagnostic statement: the same
ACT-selected nonzero shape candidate can be evaluated on a Planck lensing
readout block without refitting. It is not a physical Tau prediction, not a
Planck likelihood run, and not a dark-sector verdict.
