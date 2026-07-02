# CMB Tau Lensing Staging Promotion Precheck Contract v01

**Doc class:** staging promotion precheck contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no payload copy
**Canonical parent:** `docs/cmb_tau_lensing_submission_skeleton_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_staging_promotion_precheck_contract_v01.csv`

This contract registers a precheck for files under `payload_staging/` before
guarded promotion copies reviewed route evidence into `payloads/`. It rejects
template markers, missing required fields, mismatched route declarations,
mismatched numeric-grid hashes, and invalid numeric grid shape. It does not copy
files, does not create payloads, does not materialize replay, does not run a
score, and does not issue a dark-sector verdict.

## Commands

```text
make staging-precheck-direct
make staging-precheck-delta
make staging-precheck-failure
make staging-positive-smoke
```

The positive staging smoke temporarily fills the direct-route staging directory
with a synthetic hash-consistent route, verifies `promotion_ready=true`, and
restores the original staging skeleton. It does not copy files to `payloads/`.
Actual payload copy is only allowed through the matching
`make staging-promote-*` command after the corresponding dry run is ready.

Default generated report:

```text
data/derived/cmb_tau_lensing_staging_promotion_precheck_v01.json
```

## Claim Boundary

```text
staging_promotion_precheck_contract_only_no_payload_copy_no_score_no_dark_sector_verdict
```
