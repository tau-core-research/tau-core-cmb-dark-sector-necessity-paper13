# CMB Tau Lensing Payload Acceptance Checklist Contract v01

**Doc class:** payload acceptance checklist contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_route_evidence_pack_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_payload_acceptance_checklist_contract_v01.csv`

This contract registers a pre-submission checklist for Tau lensing route
payloads. It lists the required files, route declaration fragments, provenance
keys, hash requirements, numeric grid shape requirements, forbidden shortcuts,
and post-submission commands. It does not validate a submitted payload, does not
materialize replay, does not run a score, and does not issue a dark-sector
verdict.
For staging workflows, run the matching staging promotion precheck before
using the guarded `make staging-promote-*` command to copy reviewed files from
`payload_staging/` to `payloads/`.

## Command

```text
make payload-checklist
```

Default generated checklist:

```text
data/derived/cmb_tau_lensing_payload_acceptance_checklist_v01.json
```

## Claim Boundary

```text
payload_acceptance_checklist_contract_only_no_payload_validation_no_score_no_dark_sector_verdict
```
