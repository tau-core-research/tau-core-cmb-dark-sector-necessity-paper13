# CMB Tau Lensing Next Evidence Handoff Packet v01

**Doc class:** handoff packet
**Reader role:** Paper 13 scoring implementer
**Status:** waiting for route evidence
**Canonical parent:** `docs/cmb_tau_lensing_route_decision_evidence_receipt_audit_v01.md`

This packet gives the next executable handoff after the route evidence receipt
audit.

The route evidence intake command is tracked at:

```text
data/source_manifest/cmb_tau_lensing_route_evidence_intake_contract_v01.csv
docs/cmb_tau_lensing_route_evidence_intake_contract_v01.md
scripts/intake_tau_lensing_route_evidence.py
Makefile
```

## Immediate Choice

Choose exactly one:

```text
direct_tau_PP_grid
delta_PP_tau_against_named_fiducial_PP
explicit_failure_no_endpoint_blind_grid
```

## If Direct

Submit:

```text
payloads/tau_lensing_response_pp_grid_v01.csv
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

Then run:

```text
python3 scripts/validate_tau_lensing_grid_payload.py payloads/tau_lensing_response_pp_grid_v01.csv --route direct_tau_PP_grid
```

## If Delta

Submit:

```text
payloads/tau_lensing_response_delta_pp_v01.csv
payloads/tau_lensing_response_fiducial_pp_reference_v01.json
payloads/tau_lensing_response_grid_route_declaration_v01.md
payloads/tau_lensing_response_grid_provenance_v01.json
```

Then run:

```text
python3 scripts/validate_tau_lensing_grid_payload.py payloads/tau_lensing_response_delta_pp_v01.csv --route delta_PP_tau
```

## If Failure

Submit:

```text
payloads/tau_lensing_response_grid_failure_statement_v01.md
```

## Still Forbidden

```text
score execution
dark-sector verdict
template grid substitution
ACT/Planck residual-fitted grid
```

## Claim Boundary

```text
next_evidence_handoff_packet_only_no_selected_route_no_grid_payload_no_tau_score_no_dark_sector_verdict
```
