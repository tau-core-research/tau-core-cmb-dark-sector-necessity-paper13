# CMB Tau Lensing Projection Normalization Requirement v01

**Doc class:** projection-normalization requirement
**Reader role:** Paper 13 Tau-grid implementer
**Status:** blocked; depends on physical projection operator
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
projection_normalization_requirement_only_no_numeric_normalization_no_score_no_dark_sector_verdict
```

## Target

```text
N_projection_physical
```

## Policy

N_projection_physical is not a free post-score scale. It is the normalization implied by an accepted Projection_PP operator equation/kernel/integral, including its measure, distance/window convention, sign, units, and zero-source limit.

## Required Before Acceptance

- accepted projection_operator_rule row
- declared measure/kernel/integral normalization
- declared sign convention
- declared units or dimensionless convention
- zero-source known-limit check
- endpoint firewall certificate after value is populated

## Forbidden Sources

- post-score alpha_star
- ACT residual minimization
- Planck residual minimization
- reduced chi2 tuning
- dark-sector verdict preference

## Allowed Value Forms

- exact value derived by operator convention
- finite prior/range declared before scoring for diagnostic parameterized retry
- explicit failure if no lawful normalization can be supplied

## Evidence Links

- `docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md`
- `docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md`
- `data/derived/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.csv`
- `docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md`
- `data/derived/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.csv`

## Current Decision

```text
DO_NOT_POPULATE_N_PROJECTION_PHYSICAL_YET
```
