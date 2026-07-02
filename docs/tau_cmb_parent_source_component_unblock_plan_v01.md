# Tau CMB Parent-Source Component Unblock Plan v01

**Doc class:** parent-source component unblock plan
**Status:** PARENT_SOURCE_COMPONENT_UNBLOCK_PLAN_DECLARED_NO_COMPONENT_SUPPLIED
**Source unavailability record:** `data/derived/tau_cmb_parent_source_unavailability_record_v01.json`

## Claim Boundary

```text
tau_cmb_parent_source_component_unblock_plan_v01_plan_only_no_component_supplied_no_source_acceptance_no_phi_derivation_no_score_no_verdict
```

## Purpose

This artifact turns the clean source-unavailability stop-state into a ranked
component plan. It does not supply any component and does not accept a CMB
source. It only answers which single component should be attempted first.

## Ranked Components

- `TCMBPSUP01_001` rank 1 `morphological_seed`: endpoint-blind seed_tau_CMB_descriptor with support domain, scale/readout context, and reason it may activate the CMB route
- `TCMBPSUP01_002` rank 2 `base_field_state`: B_tau_base_CMB_descriptor with state class, allowed prior/theory source, and density-slot relation boundary
- `TCMBPSUP01_003` rank 3 `gauge_normalization_metadata`: locked units, sign, gauge, scale, and normalization policy for shared acoustic/lensing source use
- `TCMBPSUP01_004` rank 4 `response_operator_input`: R_tau_CMB input set with declared domain, codomain, and source-side dependencies
- `TCMBPSUP01_005` rank 5 `endpoint_firewall_certificate`: packet-level endpoint firewall certificate for at least one populated source component
- `TCMBPSUP01_006` rank 6 `provenance_replay_rule`: replay rule regenerating the populated component and artifact hashes without endpoint reads

## First Component

```text
morphological_seed
```

Reason:

```text
It is the shortest bridge from Tau Core morphology/readout theory to A_tau(a,k) activation without endpoint data.
```

Starting with the morphological seed is the narrowest Tau Core-specific move:
it tests whether the CMB source route has a morphology/readout activation
object before trying to define a response operator or score-facing potential.

## Status

```text
PARENT_SOURCE_COMPONENT_UNBLOCK_PLAN_DECLARED_NO_COMPONENT_SUPPLIED
```

No source acceptance, `Phi_tau_eff` derivation, score entry, no-dark claim,
Tau-response success claim, or dark-sector verdict is allowed.

## Next Minimal Unblock

```text
materialize_endpoint_blind_morphological_seed_descriptor_candidate
```
