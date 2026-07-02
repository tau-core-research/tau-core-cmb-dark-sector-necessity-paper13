# CMB Tau Lensing Staging Promotion Guard Contract v01

**Doc class:** staging promotion guard contract
**Reader role:** Paper 13 scoring implementer/reviewer
**Status:** implemented, currently blocks skeleton staging
**Canonical parent:** `docs/cmb_tau_lensing_staging_promotion_precheck_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_staging_promotion_guard_contract_v01.csv`

This contract registers the guarded promotion command from `payload_staging/`
to `payloads/`:

```text
scripts/promote_tau_lensing_staging_payload.py
```

The guard runs the route-specific staging precheck first. It copies files only
when the staging route is promotion-ready and none of the destination payload
files already exists. It never runs a score and never issues a dark-sector
verdict.

## Commands

```text
make staging-promote-direct-dry-run
make staging-promote-delta-dry-run
make staging-promote-failure-dry-run
make staging-promote-direct
make staging-promote-delta
make staging-promote-failure
```

Default report:

```text
data/derived/cmb_tau_lensing_staging_promotion_report_v01.json
```

## Allowed Decisions

```text
BLOCKED_STAGING_PRECHECK_FAILED
BLOCKED_DESTINATION_PAYLOAD_EXISTS
DRY_RUN_PROMOTION_READY
PROMOTED_TO_PAYLOADS
```

## Claim Boundary

```text
staging_promotion_guard_contract_only_no_score_no_dark_sector_verdict
```
