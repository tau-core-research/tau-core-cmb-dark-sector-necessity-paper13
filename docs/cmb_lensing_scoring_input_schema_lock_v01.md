# CMB Lensing Scoring Input Schema Lock v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** scoring-input schema lock, not a score
**Canonical parent:** `docs/cmb_source_data_extraction_dimension_audit_v01.md`

This lock chooses the smallest admissible first scoring-input path after the
source receipt, ingestion audit, and extraction/dimension audit.

## Selected First Variant

The first scoring-input path should be the ACT DR6 lensing `act_baseline`
reduced adapter:

```text
y_ACT = clkk_bandpowers_act.txt              shape (18,)
C_ACT = covmat_act.txt                       shape (18, 18)
B_ACT = binning_matrix_act.txt               shape (18, 3000)
m_ACT = B_ACT @ theory_Clkk_grid             shape (18,)
```

The corresponding reduced residual form is only a contract at this stage:

```text
chi2_ACT = (y_ACT - m_ACT)^T C_ACT^{-1} (y_ACT - m_ACT)
```

This is not yet a likelihood run and not yet a Tau Core score because no Tau
Core CMB response vector has been supplied and no `Clkk` convention has been
declared.

## Numerical Precheck

For `covmat_act.txt`:

- shape: `(18, 18)`;
- symmetry max absolute error: `0.0`;
- minimum eigenvalue: `2.3178376742959007e-18`;
- condition number: `841.9414789910932`.

This is sufficient to treat the selected covariance as numerically usable for a
later reduced adapter, pending convention and response-vector locks.

## Deferred Variants

The ACT+Planck baseline path is dimensionally plausible:

```text
ACT 18-vector + Planck 9-vector -> combined 27-vector
covmat_actplanck.txt -> shape (27, 27)
```

It is deferred because the combined vector order and Tau theory vector contract
must be locked first.

Planck TT/TE/EE binned spectra are deferred to reduced diagnostics only until a
unit/convention map and error/covariance scope are declared.

## Still Blocked

- no Tau Core `theory_Clkk_grid` or response vector is accepted yet;
- no `Clkk`/`PP` unit convention is locked;
- no lmax/binning-index contract is locked;
- no likelihood software call is made;
- no dark-sector necessity verdict is allowed.

## Claim Boundary

```text
scoring_input_schema_lock_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

The theory-convention lock is tracked at:

```text
data/source_manifest/cmb_lensing_theory_convention_lock_v01.csv
docs/cmb_lensing_theory_convention_lock_v01.md
```
