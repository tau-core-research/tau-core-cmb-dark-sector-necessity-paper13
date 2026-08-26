# ACT DR6 Lensing Tau Shape Response Controls v01

**Doc class:** nonzero Tau response control screening
**Status:** endpoint-blind analytic shape controls scored against ACT DR6 lensing adapter
**Canonical parent:** Paper 13 ACT DR6 lensing scoring route

This artifact screens a small predeclared family of nonzero Tau Core-style
lensing response controls in the locked ACT DR6 18-bin readout basis. The
control shape is analytic:

```text
s(L) = (L/L_c)^p / (1 + (L/L_c)^(p+q)), normalized to max(s)=1
y_tau(L) = A s(L)
```

The candidates use fixed amplitudes and shape parameters declared by the
script. They are diagnostic controls, not fitted physical Tau predictions.

Summary:

```text
candidate_count=12
null_chi2=2129.1187283145136
best_candidate_id=tau_shape_control_morph_lensing_broad_lowL_A1e-07
best_chi2=401.44302386760944
best_delta_chi2_vs_null=1727.675704446904
best_fractional_chi2_improvement_vs_null=0.811451086062539
best_chi2_per_naive_dof=22.30239021486719
```

## Claim Boundary

This is a shape-screening control artifact only. It does not run the ACT
likelihood, does not fit a final Tau response, does not validate Tau Core, and
does not decide dark-sector necessity.
