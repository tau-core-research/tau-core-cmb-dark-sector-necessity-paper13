# CMB Tau Lensing Submission Skeleton Contract v01

**Doc class:** submission skeleton contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, not payload
**Canonical parent:** `docs/cmb_tau_lensing_payload_acceptance_checklist_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_submission_skeleton_contract_v01.csv`

This contract registers non-payload staging skeletons for direct, delta, and
explicit failure routes. Skeletons are written under `payload_staging/`, keep a
`TEMPLATE_NOT_PAYLOAD` marker, and are not accepted by route intake. They are
only editing aids for real endpoint-blind route evidence.

## Commands

```text
make skeleton-direct
make skeleton-delta
make skeleton-failure
```

Default generated report:

```text
data/derived/cmb_tau_lensing_submission_skeleton_v01.json
```

## Boundary

Skeleton files must not be copied into `payloads/` unchanged. Real payload
submission must remove template markers, fill all required fields, compute the
numeric grid hash, and pass `make payload-checklist`, `make evidence-check`,
and `make route-submission-audit`.

## Claim Boundary

```text
submission_skeleton_contract_only_not_payload_no_score_no_dark_sector_verdict
```
