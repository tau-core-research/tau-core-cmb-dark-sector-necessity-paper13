# CMB Source Data Acquisition Status v01

**Doc class:** source data acquisition status
**Status:** official local working copies checked against receipt hashes

This artifact verifies or obtains the CMB source files listed in
`data/source_manifest/cmb_source_data_receipt_v01.csv`. The files remain local
working copies under `data/external/` and are not redistributed by the public
repository package.

Summary:

```text
receipt_rows_consumed=6
local_paths_expected=6
preexisting_local_copies=6
download_attempted_rows=0
download_succeeded_rows=0
hash_matched_rows=6
size_matched_rows=6
accepted_local_working_copy_rows=6
accepted_for_scoring_rows=0
```

## Claim Boundary

This artifact verifies source acquisition and receipt hashes only. It does not
run a CMB likelihood, does not construct a Tau prediction, does not compute a
score, and permits no no-dark or dark-sector verdict.
