# Tau CMB Source Grounding Gate v01

**Doc class:** CMB source-grounding gate
**Reader role:** Paper 13 / Tau CMB implementer
**Status:** declared but blocked; no source acceptance, no score, no verdict
**Canonical parent:** `paper13_submission_source/main.tex`
**Direct spine:** `docs/tau_cmb_cosmology_derivation_spine_v01.md`

## Claim Boundary

```text
tau_cmb_source_grounding_gate_v01_gate_only_no_cmb_source_acceptance_no_transfer_kernel_no_projection_kernel_no_score_no_dark_sector_verdict
```

## Purpose

This artifact directly binds three already-separated pieces of the program:

```text
Paper 10 source-freeze discipline
+ Tau Core morphology/readout principle
-> Paper 13 CMB derivation spine
```

It is not a new CMB source derivation. It is a gate that says what must be true
before a Tau-side CMB source may enter the formula chain

```text
rho_tau_eff(a,k)
-> Phi_tau_eff(a,k)
-> T_tau_CMB(k,a)
-> K_tau_PP(L; a,k) dmu(a,k)
-> tau_PP(L)
```

The gate preserves the Paper 10 source-freeze idea: source-side labels,
operators, and amplitudes must be fixed before endpoint residuals, scores, or
fit-improvement information are inspected.

## External Program Anchors

- Paper 10 source-freeze/source-grounding gate:
  `/Users/jolcsak/Projects/tau-core-cosmology-friedmann-readout-paper10/data/source_manifest/cosmology_source_grounding_gate_v1.csv`
- Tau Core morphology-conditioned projection principle:
  `/Users/jolcsak/Projects/tau-core-theory/source_material/tau_core_foundations/morphology_conditioned_projection_principle_v01.md`
- Tau Core morphological readout formalization:
  `/Users/jolcsak/Projects/tau-core-theory/docs/tau_core_morphological_readout_formalization_sketches_001.md`
- Paper 13 derivation spine:
  `docs/tau_cmb_cosmology_derivation_spine_v01.md`
- CMB parent-source freeze packet:
  `docs/tau_cmb_parent_source_freeze_packet_v01.md`

## Gate Rows

- `TCMBSGG01_001` `paper10_source_freeze_import`: METHOD_IMPORTED_NOT_CMB_SOURCE_ACCEPTANCE | binding: `precondition for TCMBCDS01_002 rho_tau_eff(a,k)` | blocks: rho_tau_eff cannot be promoted from a residual-selected CMB source
- `TCMBSGG01_002` `morphology_activation`: DECLARED_NOT_DERIVED_FOR_CMB | binding: `precondition for A_tau(a,k) in TCMBCDS01_002` | blocks: A_tau remains a role amplitude rather than a Tau-derived activation
- `TCMBSGG01_003` `quotient_survival`: REQUIRED_NOT_PROVED | binding: `precondition for TCMBCDS01_002 and TCMBCDS01_003` | blocks: rho_tau_eff and Phi_tau_eff cannot be distinguished from null/gauge leakage
- `TCMBSGG01_004` `closure_stability`: REQUIRED_NOT_PROVED | binding: `precondition for TCMBCDS01_003 Phi_tau_eff(a,k)` | blocks: Phi_tau_eff remains a comparison slot, not a stable Tau-side potential source
- `TCMBSGG01_005` `readout_survival`: REQUIRED_NOT_PROVED | binding: `precondition for TCMBCDS01_004 T_tau_CMB(k,a)` | blocks: T_tau_CMB cannot be treated as an available physical transfer operator
- `TCMBSGG01_006` `derivation_spine_binding`: BINDING_DECLARED_PARTIAL | binding: `TCMBCDS01_002 -> TCMBCDS01_006` | blocks: source grounding does not yet discharge kernel, measure, normalization, or zero-source obligations
- `TCMBSGG01_007` `endpoint_firewall`: REQUIRED_NOT_PASSED_FOR_POPULATED_SOURCE | binding: `precondition for TCMBCDS01_008 endpoint-blind CMB score grid` | blocks: no score, no physical Tau-route score, and no dark-sector verdict may be run from this gate

## Logical Map

```text
source-freeze
-> morphology activation
-> quotient/null survival
-> closure stability
-> CMB readout survival
-> derivation spine binding
-> endpoint firewall
-> only then: scoring-entry consideration
```

## Status

```text
SOURCE_GROUNDING_GATE_DECLARED_BLOCKED
```

This gate accepts no CMB source in v01. It supplies no `T_tau_CMB`, no
`K_tau_PP`, no projection measure, no physical normalization, and no score.
It therefore permits no no-dark claim, no Tau-response success claim, and no
dark-sector verdict.

The first concrete downstream deliverable is the parent-source freeze packet:

```text
docs/tau_cmb_parent_source_freeze_packet_v01.md
```

## Next Minimal Unblock

```text
populate_endpoint_blind_CMB_parent_source_freeze_packet_with_hashable_replay
```
