# Tau CMB Concrete R_CMB Carrier Certificate v01

**Doc class:** concrete readout carrier certificate requirements
**Status:** CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED

## Claim Boundary

```text
tau_cmb_concrete_R_CMB_carrier_certificate_v01_certificate_requirements_only_carrier_not_certified_R_CMB_not_materialized_no_score_no_likelihood_no_verdict
```

## Purpose

This artifact declares the requirements for certifying the CMB readout carrier
and concrete `R_CMB` map. It does not certify the carrier, materialize `R_CMB`,
open score entry, compute a likelihood, or decide the dark-sector question.

## Certificate Rows

- `carrier_predicate`: BLOCKED_CARRIER_PREDICATE_NOT_CERTIFIED | `C_CMB^seed`
- `domain_rule`: BLOCKED_DOMAIN_RULE_NOT_CERTIFIED | `Dom(R_CMB)`
- `codomain_role_space`: PARTIAL_CODOMAIN_AUDITED_NOT_CERTIFIED | `C_CMB^role = span/product(e_acoustic,e_density,e_lensing,e_growth,e_radiation,e_null)`
- `concrete_readout_map`: BLOCKED_CONCRETE_R_CMB_NOT_MATERIALIZED | `R_CMB : Dom(R_CMB) -> C_CMB^role`
- `null_anchor_compatibility`: BLOCKED_NULL_ANCHOR_NOT_ACCEPTED | `R_CMB(null_seed_tau_CMB) := null_readout`
- `dimension_gauge_replay`: BLOCKED_DIMENSION_GAUGE_REPLAY_NOT_CERTIFIED | `dimension/gauge/normalization replay for R_CMB`
- `endpoint_firewall`: BLOCKED_ENDPOINT_FIREWALL_REPLAY_NOT_RUN | `endpoint_blind(R_CMB materialization)`

## Status

```text
CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED
```

The first scoring-input gap is now specified as a finite certificate
requirement set. All score permissions remain closed in v01.

## Next Minimal Unblock

```text
tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01
```
