# CMB Tau Lensing Scoring Input Fulfillment Packet Contract v01

**Doc class:** scoring input fulfillment packet contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no payload acceptance, no score
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_bundle_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_scoring_input_fulfillment_packet_contract_v01.csv`

This contract registers the route-specific fulfillment packet for the remaining
Tau lensing scoring blocker. The packet lists the exact staging files, eventual
payload files, route-specific required fields, forbidden endpoint-derived
sources, and guarded promotion commands for the direct, delta, and explicit
failure routes.

It does not accept any payload, does not materialize a projection replay, does
not run a score, and does not issue a dark-sector verdict.

## Command

```text
make score-fulfillment
```

Default generated packet:

```text
data/derived/cmb_tau_lensing_scoring_input_fulfillment_packet_v01.json
```

## Current Expected Blocker

```text
real_endpoint_blind_tau_route_evidence_not_submitted
```

## Claim Boundary

```text
scoring_input_fulfillment_packet_contract_only_no_payload_acceptance_no_score_no_dark_sector_verdict
```
