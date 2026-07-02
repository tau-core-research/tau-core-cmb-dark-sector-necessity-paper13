# CMB Tau Lensing Physical Projection Operator Packet v01

**Doc class:** physical projection operator packet skeleton
**Reader role:** Paper 13 Tau-grid implementer
**Status:** codomain convention locked; no physical projection operator
**Canonical parent:** `docs/cmb_tau_lensing_projection_normalization_split_v01.md`

## Claim Boundary

```text
physical_projection_operator_packet_skeleton_only_no_operator_no_score_no_dark_sector_verdict
```

This is the concrete packet for the blocked physical projection:

```text
Projection_PP[Phi_lens_tau](L)
N_projection_physical
```

It is not the Route B adapter replay. It is the missing physics-side map from
Tau lensing-era potential/readout source into a 3000-row `PP` or `delta_PP_tau`
grid.

## Packet

```text
data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv
```

## Current Rows

- `projection_domain`: DOMAIN_CONTRACT_LOCKED_TRANSFER_DEFINITION_ONLY
- `projection_codomain`: CODOMAIN_CONVENTION_LOCKED_NO_PHYSICAL_NORMALIZATION
- `projection_operator_rule`: EXPLICIT_FAILURE_DECLARED_NO_PHYSICAL_OPERATOR_NO_SCORE
- `projection_normalization`: BLOCKED_NORMALIZATION_DEPENDS_ON_OPERATOR_RULE_REQUIREMENT_DECLARED
- `projection_replay`: BLOCKED_PHYSICAL_REPLAY_NOT_MATERIALIZABLE_REQUIREMENT_DECLARED
- `endpoint_firewall`: FIREWALL_PASS_FOR_CURRENT_SKELETON_ONLY_RERUN_AFTER_VALUES

The domain and codomain rows are locked only as contracts. The firewall row
passes only for the current skeleton and must be rerun after values are added.
The operator-rule row is closed only as an explicit non-score failure for the
current packet. The replay row distinguishes physical source-to-grid replay from
adapter replay. The normalization row remains blocked because no operator rule
supplies its measure/sign/unit convention. The domain lock does not supply a
numeric `Phi_lens_tau(a,k)` field. The codomain lock does not supply
`N_projection_physical` and does not derive `Projection_PP[Phi_lens_tau](L)`.

## Unblocks `N_projection` When

- domain and codomain conventions are accepted
- an endpoint-blind operator rule is supplied; explicit failure documents non-score closure but does not unblock
- N_projection_physical is derived before endpoint comparison
- source-to-grid replay certificate exists
- endpoint firewall certificate passes

## Decision Gate

The current operator-core decision is tracked at:

```text
docs/cmb_tau_lensing_projection_operator_decision_gate_v01.md
data/derived/cmb_tau_lensing_projection_operator_decision_gate_v01.json
```
