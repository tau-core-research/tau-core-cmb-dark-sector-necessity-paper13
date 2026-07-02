# CMB Tau Lensing Route Evidence Intake Contract v01

**Doc class:** route-evidence intake contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, no score
**Canonical parent:** `docs/cmb_tau_lensing_next_evidence_handoff_packet_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_route_evidence_intake_contract_v01.csv`

This contract adds the first executable check after route evidence is submitted.
It does not validate numeric grid values and does not project anything through
the ACT adapter. It only classifies the submitted evidence set as direct, delta,
failure, incomplete, absent, or colliding.

## Command

```text
make intake
```

Equivalent command:

```text
python3 scripts/intake_tau_lensing_route_evidence.py
```

To persist the current intake state as a generated handoff artifact:

```text
make intake-report
```

Default generated report:

```text
data/derived/cmb_tau_lensing_route_evidence_intake_report_v01.json
```

## Accepted Intake Outcome

The intake gate only advances when exactly one allowed route file set is
complete:

```text
ONE_ROUTE_ACCEPTED_FOR_NEXT_VALIDATION
```

For a direct route, the next action is direct grid validation followed by
projection replay. For a delta route, the next action is delta grid validation
followed by projection replay. For a failure route, the score remains blocked
and the failure statement becomes the current endpoint-blind blocker record.

The route-aware projection replay materializer is tracked at:

```text
data/source_manifest/cmb_tau_lensing_projection_replay_materializer_contract_v01.csv
docs/cmb_tau_lensing_projection_replay_materializer_contract_v01.md
scripts/materialize_tau_lensing_projection_replay.py
```

The route evidence firewall is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_evidence_firewall_contract_v01.csv
docs/cmb_tau_lensing_route_evidence_firewall_contract_v01.md
scripts/check_tau_lensing_route_evidence_firewall.py
```

## Blocked Intake Outcomes

The intake remains blocked when:

```text
no route evidence set is complete
more than one route evidence set is complete
only partial route files are present
```

## Claim Boundary

```text
route_evidence_intake_contract_only_no_grid_validation_no_score_no_dark_sector_verdict
```

The intake report is not a Tau score, not a likelihood run, not a projection
replay, and not a dark-sector verdict.
