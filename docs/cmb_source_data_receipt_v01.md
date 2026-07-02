# CMB Source Data Receipt v01

This receipt records local working copies of official CMB source products for
later Paper 13 scoring work. It is a provenance artifact only.

## Retrieved Sources

- Planck PR3 ancillary cosmology products from the official Planck Legacy
  Archive/IPAC release page.
- ACT DR6 lensing likelihood package v1.2 from the official NASA LAMBDA ACT
  DR6 lensing likelihood download page.
- A local snapshot of the ACT DR6 LAMBDA download page used to verify the
  tarball URL.

## Local Cache Boundary

The files under `data/external/` are local working copies. They are ignored by
git and are not part of the redistributable repository package.

The tracked artifact is the receipt:

```text
data/source_manifest/cmb_source_data_receipt_v01.csv
```

It records official URLs, source pages, byte sizes, SHA256 hashes, retrieval
status, intended use, and claim boundaries.

The follow-up ingestion audit is tracked at:

```text
data/source_manifest/cmb_source_data_ingestion_audit_v01.csv
docs/cmb_source_data_ingestion_audit_v01.md
```

## Claim Boundary

This receipt does not run a Planck, ACT, or combined CMB likelihood. It does not
compute a Tau Core score. It does not decide whether a Tau Core dark-sector
response is required.

The only accepted status is:

```text
source_data_receipt_only_no_likelihood_run_no_tau_score_no_dark_sector_verdict
```

## Next Use

The next admissible step is to build a source-data ingestion audit that checks
file formats, required spectra/likelihood components, and minimal extraction
targets before any scoring attempt.
