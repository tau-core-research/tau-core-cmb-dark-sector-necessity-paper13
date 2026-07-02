# CMB Lensing Theory Grid Alignment Audit v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** alignment sanity audit, not a score
**Canonical parent:** `docs/cmb_lensing_theory_convention_lock_v01.md`

This audit checks whether the fiducial `PP` column in the ACT DR6 lensing
package can plausibly be projected by `binning_matrix_act.txt` into the observed
ACT `clkk_bandpowers_act.txt` shape.

## Method

For several possible starting multipole alignments, the audit built a length
3000 `PP` grid from the package fiducial `lenspotentialCls` table and computed:

```text
m = B_ACT @ PP_grid
alpha = argmin || y_ACT - alpha m||
```

This is a shape/normalization sanity check only. It is not a likelihood and not
a Tau Core score.

## Result

The tested alignments all give strong shape agreement after one free scale
factor:

```text
startL=2   corr=0.9934958519276149   alpha=1.6748913335099176   rel=0.08397746671677095
startL=8   corr=0.9969513410090182   alpha=1.6823637330543197   rel=0.057755783716537924
startL=9   corr=0.9971567639879689   alpha=1.6851184009324502   rel=0.05573817823387559
startL=10  corr=0.9973017645855133   alpha=1.6882595745160942   rel=0.054243601174172706
```

The strongest candidate in this audit is `startL=10`, but this is not yet an
accepted convention. It indicates that the ACT bandpower shape is compatible
with a binned fiducial `PP`-style grid up to an unresolved normalization and
index convention.

## Still Blocked

- the package-specific column-to-multipole alignment is not proven;
- the meaning of the fitted scale factor is not proven;
- `PP` to `clkk_bandpowers` normalization is not locked;
- no Tau Core response vector has been supplied;
- no dark-sector necessity conclusion is allowed.

## Next Gate

The next admissible gate is the reduced adapter contract:

```text
y_ACT, C_ACT, B_ACT
-> accepted PP-grid convention candidate
-> explicit normalization policy
-> adapter returns diagnostic chi2 only
-> no Tau score until Tau response vector is supplied
```

## Claim Boundary

```text
alignment_audit_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

The reduced score adapter contract is tracked at:

```text
data/source_manifest/cmb_lensing_reduced_score_adapter_contract_v01.csv
docs/cmb_lensing_reduced_score_adapter_contract_v01.md
```
