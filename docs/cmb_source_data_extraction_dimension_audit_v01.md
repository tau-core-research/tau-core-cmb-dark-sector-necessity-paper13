# CMB Source Data Extraction Dimension Audit v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** extraction/dimension audit, not a score
**Canonical parent:** `docs/cmb_source_data_ingestion_audit_v01.md`

This audit checks whether the retrieved source data can be read into local
component shapes suitable for a later scoring-input schema.

## ACT DR6 Lensing

The ACT DR6 lensing likelihood tarball was extracted only into the ignored local
cache under `data/external/`. The extracted README identifies the package as
DR6 lensing likelihood data v1.2 for the ACT Collaboration lensing likelihood
software.

Observed component shapes:

- ACT `clkk_bandpowers_*`: 4 variants, each shape `(18,)`;
- Planck `clkk_bandpowers_planck`: shape `(9,)`;
- ACT covariance variants: shape `(18, 18)`;
- ACT+Planck covariance variants: shape `(27, 27)`;
- ACT binning matrix: shape `(18, 3000)`;
- Planck binning matrix: shape `(9, 3000)`.

This establishes a coherent dimension bridge for a later lensing scoring
adapter:

```text
ACT 18-vector + Planck 9-vector -> combined 27-vector
ACT covariance -> 18 x 18
ACT+Planck covariance -> 27 x 27
theory Clkk grid -> binning matrix -> bandpower vector
```

## Planck PR3 Spectra

Observed component shapes:

- baseline theory table: 2507 rows, columns `L TT TE EE BB PP`;
- TT binned table: 83 rows, columns `l Dl -dDl +dDl BestFit`;
- TE binned table: 66 rows, columns `l Dl -dDl +dDl BestFit`;
- EE binned table: 66 rows, columns `l Dl -dDl +dDl BestFit`.

These can support reduced TT/TE/EE diagnostics after a declared unit/convention
map. They do not by themselves constitute the full Planck likelihood.

## Blockers Before Scoring

- choose ACT lensing variant: baseline, extended, ACT+Planck, or CMB-marginalized;
- define vector order for combined ACT+Planck lensing inputs;
- check covariance positive-definiteness for the selected variant;
- define the theory `Clkk`/`PP` convention and lmax contract before applying
  binning matrices;
- define whether Planck binned TT/TE/EE are reduced diagnostics only or backed
  by a fuller covariance/likelihood treatment;
- provide an actual Tau Core CMB response vector to compare.

## Claim Boundary

This is not a likelihood run and not a Tau Core score. It only says the source
data are locally extractable and dimensionally plausible for the next schema
gate.

```text
extraction_dimension_audit_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

The first scoring-input schema lock is tracked at:

```text
data/source_manifest/cmb_lensing_scoring_input_schema_lock_v01.csv
docs/cmb_lensing_scoring_input_schema_lock_v01.md
```
