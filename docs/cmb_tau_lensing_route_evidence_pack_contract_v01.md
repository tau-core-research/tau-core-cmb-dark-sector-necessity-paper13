# CMB Tau Lensing Route Evidence Pack Contract v01

**Doc class:** route-evidence pack contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, templates only
**Canonical parent:** `docs/cmb_tau_lensing_scoring_todo_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_route_evidence_pack_contract_v01.csv`

This contract builds a safe submission pack for the next scoring unblock step.
It lists the exact payload paths expected by the scoring gates and maps them to
existing safe templates. It does not create real payload files and does not
mark any route as complete. Reviewed staging files may enter `payloads/` only
through the matching guarded `make staging-promote-*` workflow.

## Command

```text
make route-pack
```

Default generated pack:

```text
data/derived/cmb_tau_lensing_route_evidence_pack_v01.json
```

## Safety Rule

Templates must remain templates until real endpoint-blind evidence is filled.
Do not copy a `TEMPLATE_NOT_PAYLOAD` file into `payloads/` as a real scoring
input.
After the route-specific staging directory is filled, run the corresponding
`make staging-promote-*-dry-run` command first, then the matching
`make staging-promote-*` command only if the dry run is promotion-ready.

Numeric PP-grid templates use the same shape accepted by the validator:

```text
two numeric columns: L,value
3000 rows
L = 10..3009
```

The first column is an alignment check for humans; the validator consumes the
second column as the 3000-value response vector.

The route declaration template includes exact direct and delta blocks whose
payload paths match the firewall requirements. The template itself remains
marked `TEMPLATE_NOT_PAYLOAD` and must not be submitted unchanged.

The provenance and fiducial hash templates include the minimal JSON keys checked
by the route evidence firewall. They remain templates until all placeholder
values are replaced by endpoint-blind evidence records.

## Claim Boundary

```text
route_evidence_pack_contract_only_templates_no_payload_no_score_no_dark_sector_verdict
```
