# CMB Tau Lensing Projection Kernel/Measure Spec Scaffold v01

**Doc class:** projection kernel/measure spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** kernel/measure schema declared; no kernel accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
projection_kernel_measure_spec_scaffold_only_no_kernel_acceptance_no_grid_no_score_no_dark_sector_verdict
```

## Target Component

```text
K_tau_PP(L; a,k)dmu(a,k)
```

## Required Rows

- `TCMBPKMSS01_001` `domain_support`: REQUIRED_NOT_FILLED | required: declared a,k support for Phi_lens_tau(a,k) | failure if: support is selected after endpoint residual inspection
- `TCMBPKMSS01_002` `measure_definition`: REQUIRED_NOT_FILLED | required: dmu(a,k) or discrete sum weights | failure if: measure absorbs arbitrary amplitude or leaves normalization underdetermined
- `TCMBPKMSS01_003` `L_mapping`: REQUIRED_NOT_FILLED | required: mapping from a,k support to L=10..3009 output | failure if: L alignment is inferred from best score or bandpower residual behavior
- `TCMBPKMSS01_004` `kernel_units_and_sign`: REQUIRED_NOT_FILLED | required: units/sign role of K_tau_PP(L; a,k) | failure if: sign or units are chosen to improve fit after scoring
- `TCMBPKMSS01_005` `integrability_bound`: REQUIRED_NOT_PROVED | required: finite/integrable kernel-measure condition for every L | failure if: kernel can diverge or produce non-finite grid values without an explicit regularization rule
- `TCMBPKMSS01_006` `kernel_artifact`: REQUIRED_NOT_SUPPLIED | required: equation, table, or integral artifact with hash/provenance | failure if: kernel artifact is edited or selected using score output

## Unblocks When

- domain support is inherited from endpoint-blind Phi artifacts
- measure and L mapping are explicit
- kernel units/sign convention is dimensionally compatible with PP or delta_PP_tau
- integrability/finite replay condition is proved or enforced
- kernel artifact is hash-bound before endpoint comparison
