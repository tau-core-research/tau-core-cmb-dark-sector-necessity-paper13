# CMB Lensing Theory Convention Lock v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** theory-convention lock, not a score
**Canonical parent:** `docs/cmb_lensing_scoring_input_schema_lock_v01.md`

This lock prevents the first ACT DR6 lensing adapter from silently mixing
different lensing-spectrum conventions.

## Locked Requirement

The first reduced ACT lensing adapter may accept only a theory object with this
contract:

```text
theory_lenspotential_PP_grid: length 3000
B_ACT:                         shape (18, 3000)
m_ACT = B_ACT @ theory_lenspotential_PP_grid
```

The ACT source package contains fiducial lensing-potential style tables with a
header:

```text
L TT EE BB TE PP TP EP
```

The `PP` column is therefore the only currently admissible source-side label for
the lensing theory grid. The adapter must not rename this into a Tau Core dark
sector response until a separate Tau response mapping is supplied.

## Explicit Non-Lock

The following are not yet locked:

- whether the 3000 columns of `binning_matrix_act.txt` align to `L=0..2999`,
  `L=1..3000`, `L=2..3001`, or another package-specific convention;
- the exact normalization relation between ACT `clkk_bandpowers_*` and the
  `PP` column in the fiducial lensing-potential tables;
- whether a Tau Core response should be added to, replace, or reparameterize the
  fiducial `PP` grid;
- any physical dark-sector necessity conclusion.

## Why This Matters

The extracted ACT files are dimensionally compatible, but a dimension match is
not yet a physics convention match. A one-bin index shift or a wrong
normalization of the lensing-potential spectrum would produce a meaningless
score.

## Next Gate

The next admissible gate is:

```text
theory PP grid
-> binning matrix index alignment
-> normalization check against fiducial bandpower scale
-> reduced adapter contract
-> only then score attempt
```

## Claim Boundary

```text
theory_convention_lock_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

The first theory-grid alignment audit is tracked at:

```text
data/source_manifest/cmb_lensing_theory_grid_alignment_audit_v01.csv
docs/cmb_lensing_theory_grid_alignment_audit_v01.md
```
