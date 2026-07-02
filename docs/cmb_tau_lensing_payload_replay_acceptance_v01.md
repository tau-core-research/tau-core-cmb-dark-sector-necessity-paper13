# CMB Tau Lensing Payload Replay Acceptance v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** replay acceptance gate, blocked
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_plan_v01.md`

This gate replays the fourth unblock step before any reduced Tau lensing score
attempt. It checks whether the required Phi source, transfer, and PP-grid
payloads have been submitted and can be accepted with hashes and firewall
statements.

## Result

```text
REPLAY_BLOCKED_PAYLOADS_NOT_SUBMITTED
```

No Tau lensing score can be run from this replay state.

## Blocking Inputs

- Phi source payload is accepted for transfer definition only by
  `cmb_tau_lensing_phi_source_acceptance_audit_v02.csv`, but it is not accepted
  as a numeric score input.
- Transfer payload is accepted for projection definition only by
  `cmb_tau_lensing_transfer_acceptance_audit_v02.csv`, but no numeric transfer
  kernel is accepted for score.
- PP-grid rule components are partially submitted and audited by
  `cmb_tau_lensing_pp_grid_acceptance_audit_v02.csv`, but the numeric grid and
  projection replay are missing.
- No score-eligible payload hashes can be replayed yet.
- No endpoint-blind score firewall replay can pass until the PP-grid payload
  exists.

## Claim Boundary

```text
payload_replay_acceptance_only_no_payload_no_tau_score_no_dark_sector_verdict
```

This artifact is a readiness gate only. It does not evaluate ACT, Planck, Tau
Core dark-sector necessity, or a physical Tau response.
