# CMB Source Data Ingestion Audit v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** source-ingestion audit, not a score
**Canonical parent:** `docs/cmb_source_data_receipt_v01.md`

This audit asks the narrow question: do the retrieved official source-data
objects contain components that can support the next scoring-input extraction
step?

## Result

The answer is yes, but only at ingestion-readiness level.

The Planck PR3 files provide:

- binned TT, TE, and EE observable tables with `l`, `Dl`, lower/upper errors,
  and `BestFit` columns;
- a baseline theory table with `L`, `TT`, `TE`, `EE`, `BB`, and `PP` columns.

The ACT DR6 lensing likelihood tarball contains:

- 5 `clkk_bandpowers_*` files;
- 6 `covmat_*` files;
- 2 `binning_matrix_*` files;
- 18 likelihood-correction or fiducial-spectrum entries.

## Scoring Boundary

No score is accepted at this stage. The audit only establishes that source
objects exist locally, match the receipt hashes, and contain plausible component
classes for a later scoring adapter.

Blocked before scoring:

- Planck reduced diagnostics need an explicit unit/convention map for `Dl`,
  `Cl`, and lensing `PP`;
- Planck binned spectra need a declared covariance/error model if used beyond
  a reduced diagnostic;
- ACT lensing requires extraction into a local cache and a dimension check
  across bandpowers, covariance matrices, and binning matrices;
- no Tau Core CMB response vector has been evaluated against these data.

## Next Gate

The next admissible gate is an extraction audit:

```text
source receipt
-> tar/table inventory
-> local extraction cache
-> dimension/shape validation
-> scoring-input schema
-> only then scoring
```

The current claim boundary remains:

```text
ingestion_audit_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

The extraction/dimension audit is tracked at:

```text
data/source_manifest/cmb_source_data_extraction_dimension_audit_v01.csv
docs/cmb_source_data_extraction_dimension_audit_v01.md
```
