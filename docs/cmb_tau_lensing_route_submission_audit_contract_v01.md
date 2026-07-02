# CMB Tau Lensing Route Submission Audit Contract v01

**Doc class:** route submission audit contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_route_evidence_firewall_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_route_submission_audit_contract_v01.csv`

This contract registers a compact pre-replay audit over route intake and the
route evidence firewall. It does not call the downstream score-readiness
pipeline, does not validate numeric grid values, does not materialize projection
replay, does not run a score, and does not issue a dark-sector verdict.

## Command

```text
make route-submission-audit
```

Default generated audit:

```text
data/derived/cmb_tau_lensing_route_submission_audit_v01.json
```

## Decisions

```text
BLOCKED_SUBMIT_EXACTLY_ONE_ROUTE
BLOCKED_REPAIR_ROUTE_EVIDENCE_FIREWALL
NUMERIC_ROUTE_READY_FOR_MATERIALIZE_REPLAY
FAILURE_ROUTE_RECORDED_SCORE_REMAINS_BLOCKED
```

The bad-route firewall smoke checks the `BLOCKED_REPAIR_ROUTE_EVIDENCE_FIREWALL`
decision with a synthetic direct route whose provenance hash does not match the
submitted grid. That smoke path does not leave payload files behind.

The good-route smoke checks the `NUMERIC_ROUTE_READY_FOR_MATERIALIZE_REPLAY`
decision with a synthetic hash-consistent zero grid. That path validates gate
plumbing only; it is not physical Tau evidence and does not leave payload files
behind.

## Claim Boundary

```text
route_submission_audit_contract_only_no_grid_validation_no_score_no_dark_sector_verdict
```
