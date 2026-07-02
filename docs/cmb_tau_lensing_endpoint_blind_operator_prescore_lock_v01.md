# CMB Tau Lensing Endpoint-Blind Operator Prescore Lock v01

**Doc class:** physical Tau-route prescore lock
**Reader role:** Paper 13 Tau-grid implementer
**Status:** PHYSICAL_TAU_ROUTE_PRESCORE_LOCKED
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_v01.md`

## Claim Boundary

```text
endpoint_blind_operator_prescore_lock_only_no_physical_score_no_dark_sector_verdict
```

## Lock Result

```text
pre_score_locked
score_attempt_allowed_for_physical_tau_route = False
```

## Lock Reasons

- `operator_packet_content_audit_not_accepted`
- `projection_operator_decision_gate_does_not_allow_physical_score`

## Inputs

```text
receipt_status = OPERATOR_PACKET_RECEIPT_AUDIT_READY_FOR_CONTENT_AUDITS
receipt_decision = ROUTE_TO_CONTENT_AUDITS_NOT_SCORE
content_router_status = CONTENT_AUDIT_ROUTER_READY_NOT_SCORE
content_audit_status = CONTENT_AUDIT_BLOCKED_PARTIAL_CANDIDATE_NOT_ACCEPTED
operator_gate_decision = DO_NOT_SCORE_EXPLICIT_OPERATOR_FAILURE
```

## Next Minimal Unblock

```text
supply_full_kernel_measure_and_normalization_then_fill_dimension_firewall_audits
```

This lock is scoped to the endpoint-blind physical Tau-route. It does not claim
that other reduced diagnostic or synthetic smoke-test routes are physically
accepted.
