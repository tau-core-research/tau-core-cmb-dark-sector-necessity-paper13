# CMB Lensing Reduced Score Adapter Contract v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** reduced adapter contract, not a Tau score
**Canonical parent:** `docs/cmb_lensing_theory_grid_alignment_audit_v01.md`

This contract defines the smallest diagnostic ACT DR6 lensing adapter that can
be implemented before any Tau Core response vector is accepted.

## Diagnostic Adapter

Inputs:

```text
y_ACT: observed ACT DR6 clkk bandpowers, shape (18,)
C_ACT: ACT covariance, shape (18, 18)
B_ACT: ACT binning matrix, shape (18, 3000)
PP_grid: lensing-potential style theory grid, shape (3000,)
```

Diagnostic model:

```text
m_ACT = B_ACT @ PP_grid
alpha = argmin ||y_ACT - alpha m_ACT||
chi2_diag = (y_ACT - alpha m_ACT)^T C_ACT^{-1} (y_ACT - alpha m_ACT)
```

This diagnostic may be used only as an adapter sanity check. The free `alpha`
absorbs unresolved normalization and must not be reinterpreted as a physical Tau
Core parameter without a separate parameter policy.

## Sanity Check

Using the best current alignment candidate from the prior audit:

```text
startL = 10
alpha = 1.6882595745160942
chi2_diag = 22.437225603889548
naive dof = 17
chi2 / dof = 1.319836800228797
```

This shows that the adapter formula and covariance solve are numerically usable.
It does not validate Tau Core.

## Tau Response Gate

A Tau score is blocked until one of the following is supplied:

```text
tau_theory_lenspotential_PP_grid: shape (3000,)
```

or a declared perturbative form:

```text
tau_PP_grid = PP_fiducial + delta_PP_tau
```

For Tau scoring, no post-hoc free scale is allowed unless the scale is declared
in advance as a model parameter with a stated prior/range. Otherwise the score
would measure fitting freedom rather than theory content.

## Claim Boundary

```text
reduced_score_adapter_contract_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

The Tau response vector requirement gate is tracked at:

```text
data/source_manifest/cmb_tau_lensing_response_vector_requirement_v01.csv
docs/cmb_tau_lensing_response_vector_requirement_v01.md
```

The current Tau response score gate is tracked at:

```text
data/source_manifest/cmb_tau_lensing_response_score_gate_v01.csv
docs/cmb_tau_lensing_response_score_gate_v01.md
```

The ACT-side scoring environment check is tracked at:

```text
data/source_manifest/cmb_tau_lensing_scoring_environment_contract_v01.csv
docs/cmb_tau_lensing_scoring_environment_contract_v01.md
scripts/check_tau_lensing_scoring_environment.py
```
