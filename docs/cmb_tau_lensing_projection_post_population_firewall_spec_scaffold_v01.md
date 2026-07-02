# CMB Tau Lensing Projection Post-Population Firewall Spec Scaffold v01

**Doc class:** projection post-population firewall spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** firewall schema declared; not run; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`

## Claim Boundary

```text
projection_post_population_firewall_spec_scaffold_only_no_firewall_pass_no_score_no_dark_sector_verdict
```

## Scope

```text
firewall requirements after operator, kernel, normalization, and output grid values are populated
```

This is not the current skeleton certificate:

```text
current skeleton PASS_FOR_CURRENT_SKELETON_ONLY remains separate
```

## Required Rows

- `TCMBPPFSS01_001` `operator_artifact_firewall`: REQUIRED_AFTER_VALUES | required: operator/equation artifact created without score, residual, or verdict inputs | failure if: operator artifact cites alpha_star, chi2, residuals, or score outputs
- `TCMBPPFSS01_002` `kernel_measure_firewall`: REQUIRED_AFTER_VALUES | required: kernel/measure artifact created without endpoint fit feedback | failure if: kernel choices are selected to improve bandpower agreement
- `TCMBPPFSS01_003` `normalization_firewall`: REQUIRED_AFTER_VALUES | required: N_projection_physical value/range provenance excludes post-score scaling | failure if: normalization is set from post-score alpha_star or residual minimization
- `TCMBPPFSS01_004` `output_grid_firewall`: REQUIRED_AFTER_VALUES | required: 3000-row grid replay excludes score outputs and hand-fit edits | failure if: grid values are edited after score or selected from endpoint performance
- `TCMBPPFSS01_005` `route_choice_firewall`: REQUIRED_AFTER_VALUES | required: direct PP versus delta route chosen before endpoint score | failure if: route choice is switched after comparing score outcomes
- `TCMBPPFSS01_006` `score_separation_firewall`: REQUIRED_AFTER_VALUES | required: physical projection replay completed before guarded score execution | failure if: score execution precedes or participates in projection construction
