# CMB Tau Lensing Projection Normalization Spec Scaffold v01

**Doc class:** projection normalization spec scaffold
**Reader role:** Paper 13 Tau-grid implementer
**Status:** normalization schema declared; no numeric normalization accepted; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_normalization_requirement_v01.md`

## Claim Boundary

```text
projection_normalization_spec_scaffold_only_no_numeric_normalization_no_score_no_dark_sector_verdict
```

## Target

```text
N_projection_physical
```

## Required Rows

- `TCMBPNSS01_001` `normalization_role`: REQUIRED_NOT_FILLED | required: state whether N_projection_physical is fixed by operator convention or is a pre-score diagnostic parameter | failure if: normalization role is chosen after seeing alpha_star, residuals, or chi2
- `TCMBPNSS01_002` `finite_value_or_range`: REQUIRED_NOT_FILLED | required: finite exact value or finite prior/range | failure if: normalization is unbounded, NaN/inf, or post-score fitted
- `TCMBPNSS01_003` `unit_dimension_role`: REQUIRED_NOT_FILLED | required: units or dimensionless convention for N_projection_physical | failure if: normalization silently absorbs unresolved unit mismatch
- `TCMBPNSS01_004` `sign_convention`: REQUIRED_NOT_FILLED | required: sign role of positive/negative Tau contribution | failure if: sign is selected to improve endpoint fit
- `TCMBPNSS01_005` `zero_source_compatibility`: REQUIRED_NOT_PROVED | required: finite normalization participates in zero-source limit proof | failure if: normalization introduces a source-independent additive term
- `TCMBPNSS01_006` `provenance_firewall`: REQUIRED_NOT_SUPPLIED | required: hash/provenance/firewall record for normalization choice | failure if: normalization cites endpoint score products or derived post-score alpha

## Allowed Value Forms

- operator-implied exact finite value
- endpoint-blind finite diagnostic prior/range
- explicit failure if no lawful normalization exists

## Forbidden Sources

- post-score alpha_star
- ACT/Planck residual minimization
- reduced chi2 tuning
- dark-sector verdict preference
